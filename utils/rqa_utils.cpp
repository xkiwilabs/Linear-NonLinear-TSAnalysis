// rqa_utils.cpp
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>

#include <cmath>
#include <vector>
#include <stdexcept>
#include <algorithm>
#include <numeric>
#include <map>
#include <string>

namespace py = pybind11;

/************************************
 * rqa_dist
 *
 * Compute distances between all points of two vectors,
 * which are embedded using time lags.
 ************************************/
py::dict rqa_dist(py::array_t<float> a, py::array_t<float> b, int dim, int lag) {
    auto buf_a = a.request();
    auto buf_b = b.request();
    if (buf_a.ndim < 1 || buf_b.ndim < 1)
        throw std::runtime_error("Input arrays must have at least one dimension.");

    int n = buf_a.shape[0];
    int n2 = n - lag * (dim - 1);
    if (n2 <= 0)
        throw std::runtime_error("Not enough data for these embedding parameters.");

    float* ptr_a = static_cast<float*>(buf_a.ptr);
    float* ptr_b = static_cast<float*>(buf_b.ptr);

    auto result = py::array_t<float>({n2, n2});
    auto buf_res = result.request();
    float* res_ptr = static_cast<float*>(buf_res.ptr);

    if (dim > 1) {
        std::vector<float> emb_a(n2 * dim);
        std::vector<float> emb_b(n2 * dim);
        for (int k = 0; k < dim; k++) {
            for (int i = 0; i < n2; i++) {
                emb_a[i * dim + k] = ptr_a[lag * k + i];
                emb_b[i * dim + k] = ptr_b[lag * k + i];
            }
        }
        for (int i = 0; i < n2; i++) {
            for (int j = 0; j < n2; j++) {
                float sum_sq = 0.0f;
                for (int k = 0; k < dim; k++) {
                    float diff = emb_a[i * dim + k] - emb_b[j * dim + k];
                    sum_sq += diff * diff;
                }
                res_ptr[i * n2 + j] = std::sqrt(sum_sq);
            }
        }
    } else {
        for (int i = 0; i < n2; i++) {
            for (int j = 0; j < n2; j++) {
                res_ptr[i * n2 + j] = std::fabs(ptr_a[i] - ptr_b[j]);
            }
        }
    }

    py::dict ds;
    ds["dim"] = dim;
    ds["lag"] = lag;
    ds["d"] = result;
    return ds;
}

/************************************
 * rqa_radius
 *
 * Threshold a square distance matrix.
 * 
 * The parameter diag_ignore indicates how many diagonals to zero out:
 *   - For auto RQA, 1 ignores the main diagonal only,
 *     2 ignores the main diagonal and one off-diagonal on each side, etc.
 *   - For cross RQA, diag_ignore should be 0.
 ************************************/
py::array_t<int8_t> rqa_radius(py::array_t<float> dist, int rescale, float rad, int diag_ignore) {
    auto buf = dist.request();
    if (buf.ndim != 2 || buf.shape[0] != buf.shape[1])
        throw std::runtime_error("Distance matrix must be square");

    int n = buf.shape[0];
    if (buf.size == 1)
        throw std::runtime_error("Distance matrix has only one element!");
    if (rad <= 0)
        throw std::runtime_error("Please use a scalar threshold > 0");
    if (diag_ignore < 0)
        throw std::runtime_error("Please use a non-negative integer for diag_ignore");

    float* dist_ptr = static_cast<float*>(buf.ptr);
    std::vector<float> scaled(buf.size);
    for (size_t i = 0; i < buf.size; i++) {
        scaled[i] = dist_ptr[i];
    }

    if (rescale == 1) {
        double sum = std::accumulate(scaled.begin(), scaled.end(), 0.0);
        double mean_val = sum / scaled.size();
        for (auto &v : scaled)
            v = v / mean_val;
    } else if (rescale == 2) {
        float max_val = *std::max_element(scaled.begin(), scaled.end());
        for (auto &v : scaled)
            v = v / max_val;
    }

    auto thrd = py::array_t<int8_t>({n, n});
    auto buf_thrd = thrd.request();
    int8_t* thrd_ptr = static_cast<int8_t*>(buf_thrd.ptr);
    for (int i = 0; i < n * n; i++) {
        thrd_ptr[i] = (scaled[i] <= rad) ? 1 : 0;
    }

    // Zero out the diagonals (Theiler window) based on diag_ignore.
    if (diag_ignore != 0) {
        for (int d = 0; d < diag_ignore; d++) {
            for (int j = 0; j < n - d; j++) {
                thrd_ptr[j * n + (j + d)] = 0;     // upper diagonal at offset d
                thrd_ptr[(j + d) * n + j] = 0;       // lower diagonal at offset d
            }
        }
    }

    return thrd;
}

/************************************
 * rqa_line
 *
 * Find all diagonal lines (and compute trend measures)
 * in a thresholded matrix.
 *
 * The parameter diag_ignore specifies the number of diagonals to ignore.
 ************************************/
py::tuple rqa_line(py::array_t<int8_t> thrd, int diag_ignore) {
    auto buf = thrd.request();
    if (buf.ndim != 2 || buf.shape[0] != buf.shape[1])
        throw std::runtime_error("Thresholded distance matrix must be square");

    int n = buf.shape[0];
    int possnumll = (n * n) / 2;
    std::vector<short> ll(possnumll, 0);
    int diagCount = 2 * n - 1;
    std::vector<std::vector<float>> recur(diagCount, std::vector<float>(2, 0.0f));
    int nlines = 0;
    int8_t* data = static_cast<int8_t*>(buf.ptr);

    for (int i = 0; i < diagCount; i++) {
        int offset = i - n + 1;
        int ld = n - std::abs(offset);
        recur[i][0] = ld;
        int j = 0;
        while (j < ld) {
            int row, col;
            if (offset >= 0) {
                row = j;
                col = j + offset;
            } else {
                row = j - offset;
                col = j;
            }
            int index = row * n + col;
            if (data[index] == 1) {
                nlines++;
                if(nlines > possnumll)
                    nlines = possnumll;
                ll[nlines - 1] = 1;
                recur[i][1] += 1;
                int k = j + 1;
                while (k < ld) {
                    int r, c;
                    if (offset >= 0) {
                        r = k;
                        c = k + offset;
                    } else {
                        r = k - offset;
                        c = k;
                    }
                    int idx = r * n + c;
                    if (data[idx] == 1) {
                        ll[nlines - 1] += 1;
                        recur[i][1] += 1;
                        k++;
                    } else {
                        break;
                    }
                }
                j = k;
            } else {
                j++;
            }
        }
    }
    ll.resize(nlines);

    int mid = 0;
    float max_val = recur[0][0];
    for (int i = 1; i < diagCount; i++) {
        if (recur[i][0] > max_val) {
            max_val = recur[i][0];
            mid = i;
        }
    }
    for (int i = 0; i < diagCount; i++) {
        if (recur[i][0] != 0)
            recur[i][1] = recur[i][1] / recur[i][0];
    }

    // Lower diagonal trend
    int first = diag_ignore;
    int last = n - 1;
    int len_range = last - first + 1;
    std::vector<double> x_lower, y_lower;
    for (int i = 0; i < len_range; i++) {
        x_lower.push_back(first + i);
        int idx = mid - diag_ignore - i;
        if (idx < 0)
            break;
        y_lower.push_back(100.0 * recur[idx][1]);
    }
    double trend1 = 0.0;
    if (y_lower.size() >= 2) {
        double sum_x = std::accumulate(x_lower.begin(), x_lower.end(), 0.0);
        double sum_y = std::accumulate(y_lower.begin(), y_lower.end(), 0.0);
        double sum_xx = 0.0, sum_xy = 0.0;
        int valid_count = y_lower.size();
        for (size_t i = 0; i < valid_count; i++) {
            sum_xx += x_lower[i] * x_lower[i];
            sum_xy += x_lower[i] * y_lower[i];
        }
        double denom = valid_count * sum_xx - sum_x * sum_x;
        if (denom != 0)
            trend1 = 1000 * ((valid_count * sum_xy - sum_x * sum_y) / denom);
    }

    // Upper diagonal trend
    int first_up = mid + diag_ignore;
    int last_up = 2 * n - 2;
    int len_range_up = last_up - first_up + 1;
    std::vector<double> x_upper, y_upper;
    for (int i = 0; i < len_range_up; i++) {
        x_upper.push_back(diag_ignore + i);
        if (first_up + i >= diagCount)
            break;
        y_upper.push_back(100.0 * recur[first_up + i][1]);
    }
    double trend2 = 0.0;
    if (y_upper.size() >= 2) {
        double sum_x = std::accumulate(x_upper.begin(), x_upper.end(), 0.0);
        double sum_y = std::accumulate(y_upper.begin(), y_upper.end(), 0.0);
        double sum_xx = 0.0, sum_xy = 0.0;
        int valid_count = y_upper.size();
        for (size_t i = 0; i < valid_count; i++) {
            sum_xx += x_upper[i] * x_upper[i];
            sum_xy += x_upper[i] * y_upper[i];
        }
        double denom = valid_count * sum_xx - sum_x * sum_x;
        if (denom != 0)
            trend2 = 1000 * ((valid_count * sum_xy - sum_x * sum_y) / denom);
    }

    int maxl_poss = n - diag_ignore;
    int npts = (diag_ignore == 0) ? n * n : n * n - n - 2 * n * (diag_ignore - 1) + diag_ignore * (diag_ignore - 1);

    auto ll_array = py::array_t<short>(ll.size());
    auto buf_ll = ll_array.request();
    short* ll_ptr = static_cast<short*>(buf_ll.ptr);
    for (size_t i = 0; i < ll.size(); i++)
        ll_ptr[i] = ll[i];

    return py::make_tuple(ll_array, maxl_poss, npts, trend1, trend2);
}

/************************************
 * rqa_histlines
 *
 * Compute the histogram of line lengths and basic statistics.
 ************************************/
py::tuple rqa_histlines(py::array_t<short> llengths, int minl) {
    auto buf = llengths.request();
    if (buf.ndim != 1)
        throw std::runtime_error("Input data must be a vector, not a matrix");
    if (minl <= 0)
        throw std::runtime_error("Please use an integer min line length >= 1");

    short* data = static_cast<short*>(buf.ptr);
    size_t size = buf.shape[0];

    std::vector<short> valid;
    for (size_t i = 0; i < size; i++) {
        if (data[i] >= minl)
            valid.push_back(data[i]);
    }
    if (valid.empty()) {
        auto linehist = py::array_t<float>({1, 2});
        auto buf_hist = linehist.request();
        float* hist_ptr = static_cast<float*>(buf_hist.ptr);
        hist_ptr[0] = 0;
        hist_ptr[1] = 0;
        py::list linestats;
        linestats.append(0.0);
        linestats.append(0.0);
        linestats.append(0);
        return py::make_tuple(linehist, linestats);
    }

    double sum = std::accumulate(valid.begin(), valid.end(), 0.0);
    double mean_val = sum / valid.size();
    double sq_sum = 0.0;
    for (auto v : valid)
        sq_sum += (v - mean_val) * (v - mean_val);
    double std_val = std::sqrt(sq_sum / valid.size());
    int count = valid.size();
    py::list linestats;
    linestats.append(mean_val);
    linestats.append(std_val);
    linestats.append(count);

    std::map<short, int> freq;
    for (auto v : valid)
        freq[v]++;
    size_t num_unique = freq.size();
    auto linehist = py::array_t<float>({(int)num_unique, 2});
    auto buf_hist = linehist.request();
    float* hist_ptr = static_cast<float*>(buf_hist.ptr);
    size_t idx = 0;
    for (auto& kv : freq) {
        hist_ptr[idx * 2]     = kv.first;
        hist_ptr[idx * 2 + 1] = kv.second;
        idx++;
    }
    return py::make_tuple(linehist, linestats);
}

/************************************
 * rqa_entropy
 *
 * Compute the Shannon entropy of a distribution.
 ************************************/
py::list rqa_entropy(py::array_t<float> distr, int nstates) {
    auto buf = distr.request();
    if (buf.ndim != 1)
        throw std::runtime_error("Input data must be a vector, not a matrix");
    if (nstates <= 0)
        throw std::runtime_error("Please use an integer greater than 0 for the number of states");

    float* data = static_cast<float*>(buf.ptr);
    size_t size = buf.shape[0];
    double sum_val = 0.0;
    for (size_t i = 0; i < size; i++)
        sum_val += data[i];
    if (sum_val == 0.0)
        throw std::runtime_error("Sum of the distribution is zero; invalid input.");

    double shannon_entropy = 0.0;
    for (size_t i = 0; i < size; i++) {
        double p = data[i] / sum_val;
        if (p > 0)
            shannon_entropy -= p * std::log(p) / std::log(2.0);
    }
    double max_entropy = std::log(nstates) / std::log(2.0);
    double remaining_info = max_entropy - shannon_entropy;
    py::list result;
    result.append(shannon_entropy);
    result.append(remaining_info);
    return result;
}

/************************************
 * rqa_stats
 *
 * Perform full Recurrence Quantification Analysis (RQA) on a distance matrix.
 *
 * New parameters:
 *   - rqa_mode: a string ("auto" or "cross"). If "auto", the main diagonal (and optionally off-diagonals)
 *               are ignored. For "cross", no diagonals are ignored.
 *   - diag_ignore: if rqa_mode is "auto", this determines how many diagonals to ignore (1 = main diagonal only, etc.)
 ************************************/
py::tuple rqa_stats(py::array_t<float> d, int rescale, float rad, int diag_ignore, int minl, std::string rqa_mode="auto") {
    int err_code = 0;
    // For cross recurrence, ignore no diagonals.
    if (rqa_mode == "cross")
        diag_ignore = 0;

    py::array_t<int8_t> td;
    try {
        td = rqa_radius(d, rescale, rad, diag_ignore);
    } catch (std::runtime_error &e) {
        throw std::runtime_error("Error in thresholding: " + std::string(e.what()));
        err_code = 1;
        return py::make_tuple(py::none(), py::none(), py::none(), err_code);
    }
    py::tuple line_result = rqa_line(td, diag_ignore);
    py::array ll = line_result[0].cast<py::array>();
    int maxl_poss = line_result[1].cast<int>();
    int npts = line_result[2].cast<int>();
    double trend1 = line_result[3].cast<double>();
    double trend2 = line_result[4].cast<double>();

    if (ll.request().size == 0) {
        throw std::runtime_error("Error in line counting.");
        err_code = 2;
        return py::make_tuple(py::none(), py::none(), py::none(), err_code);
    }
    py::tuple hist_result = rqa_histlines(ll, minl);
    py::array lh = hist_result[0].cast<py::array>();
    py::list llmnsd = hist_result[1].cast<py::list>();

    py::list entropy;
    if (lh.request().size > 2) {
        auto buf_lh = lh.request();
        int rows = buf_lh.shape[0];
        std::vector<float> freq(rows);
        float* lh_ptr = static_cast<float*>(buf_lh.ptr);
        for (int i = 0; i < rows; i++) {
            freq[i] = lh_ptr[i * 2 + 1];
        }
        auto freq_array = py::array_t<float>({rows});
        auto buf_freq = freq_array.request();
        float* freq_ptr = static_cast<float*>(buf_freq.ptr);
        for (int i = 0; i < rows; i++)
            freq_ptr[i] = freq[i];
        entropy = rqa_entropy(freq_array, maxl_poss - minl + 1);
    } else {
        entropy = py::list();
        entropy.append(0.0);
        entropy.append(0.0);
    }

    auto buf_ll = ll.request();
    short* ll_ptr = static_cast<short*>(buf_ll.ptr);
    long long recur_sum = 0;
    for (size_t i = 0; i < buf_ll.size; i++)
        recur_sum += ll_ptr[i];
    double perc_rec = 100.0 * recur_sum / npts;
    double perc_determ = 0.0;
    double maxl_found = 0.0;
    if (lh.request().size > 0) {
        auto buf_lh = lh.request();
        int rows = buf_lh.shape[0];
        double sum_det = 0.0;
        for (int i = 0; i < rows; i++) {
            float l_val = static_cast<float*>(buf_lh.ptr)[i * 2];
            float count_val = static_cast<float*>(buf_lh.ptr)[i * 2 + 1];
            sum_det += l_val * count_val;
            if (l_val > maxl_found)
                maxl_found = l_val;
        }
        perc_determ = 100.0 * sum_det / recur_sum;
    }

    py::dict rs;
    rs["rescale"]     = rescale;
    rs["rad"]         = rad;
    rs["diag_ignore"] = diag_ignore;
    rs["minl"]        = minl;
    rs["perc_recur"]  = perc_rec;
    rs["perc_determ"] = perc_determ;
    rs["npts"]        = npts;
    rs["entropy"]     = entropy;
    rs["maxl_poss"]   = maxl_poss;
    rs["maxl_found"]  = maxl_found;
    rs["trend1"]      = trend1;
    rs["trend2"]      = trend2;
    rs["llmnsd"]      = llmnsd;

    py::dict mats;
    mats["rescale"] = rescale;
    mats["rad"]     = rad;
    mats["diag_ignore"] = diag_ignore;
    mats["minl"]    = minl;
    mats["td"]      = td;
    mats["ll"]      = ll;
    mats["lh"]      = lh;

    return py::make_tuple(td, rs, mats, err_code);
}

/************************************
 * Module definition
 ************************************/
PYBIND11_MODULE(rqa_utils_cpp, m) {
    m.doc() = "High-performance RQA utilities implemented in C++ using pybind11";

    m.def("rqa_dist", &rqa_dist,
          "Compute distances between embedded vectors",
          py::arg("a"), py::arg("b"), py::arg("dim"), py::arg("lag"));

    m.def("rqa_radius", &rqa_radius,
          "Threshold the distance matrix",
          py::arg("dist"), py::arg("rescale"), py::arg("rad"), py::arg("diag_ignore"));

    m.def("rqa_line", &rqa_line,
          "Find diagonal lines and compute trends in a thresholded matrix",
          py::arg("thrd"), py::arg("diag_ignore"));

    m.def("rqa_histlines", &rqa_histlines,
          "Compute the histogram of line lengths and stats",
          py::arg("llengths"), py::arg("minl"));

    m.def("rqa_entropy", &rqa_entropy,
          "Compute Shannon entropy of a distribution",
          py::arg("distr"), py::arg("nstates"));

    m.def("rqa_stats", &rqa_stats,
          "Perform full RQA analysis on a distance matrix",
          py::arg("d"), py::arg("rescale"), py::arg("rad"),
          py::arg("diag_ignore"), py::arg("minl"), py::arg("rqa_mode") = "auto");
}
