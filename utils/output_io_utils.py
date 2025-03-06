# Function: Write stats to file
def write_rqa_stats(filename, params, rs, err_code):
    with open("RQA_Stats.csv", "a") as f:
        f.write(f"{filename}, {params['eDim']}, {params['tLag']}, {params['rescaleNorm']}, {params['radius'] * 100}, ")
        if err_code == 0:
            f.write(f"{rs['perc_recur']:.3f}, {rs['perc_determ']:.3f}, {rs['maxl_found']:.3f}, "
                    f"{rs['llmnsd'][0]:.3f}, {rs['entropy'][0]:.3f}\n")
        else:
            f.write("0.0, 0.0, 0.0, 0.0, 0.0\n")