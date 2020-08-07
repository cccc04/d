import argparse
import datetime

input_links = 24
output_links = 24

def extract_from_header(header_file, parameter):
    fp = open(header_file, "r")
    if (fp.mode != "r"): raise Exception("Failed to open " + header_file)

    for cnt, line in enumerate(fp):
        r = line.split();
        if (len(r) == 3 and r[1] == parameter):
            return int(r[2])

    raise Exception("Cannot extract parameter '" + parameter + "' from header")

def generate_algo_top_wrapper(filename, hls_input_links, hls_output_links):
    with open(filename, "w") as f:
        f.write("-- This file is automatically generated and maintained, DO NOT MODIFY!\n")
        f.write("\n")
        f.write("library IEEE;\n")
        f.write("use IEEE.STD_LOGIC_1164.all;\n")
        f.write("\n")
        f.write("use work.algo_pkg.all;\n")
        f.write("\n")
        f.write("entity algo_top_wrapper is\n")
        f.write("  generic (\n")
        f.write("    N_INPUT_LINKS  : integer := 24;\n")
        f.write("    N_OUTPUT_LINKS : integer := 24\n")
        f.write("    );\n")
        f.write("  port (\n")
        f.write("    -- Algo Control/Status Signals\n")
        f.write("    ap_clk   : in  std_logic;\n")
        f.write("    ap_rst   : in  std_logic;\n")
        f.write("    ap_start : in  std_logic;\n")
        f.write("    ap_done  : out std_logic;\n")
        f.write("    ap_idle  : out std_logic;\n")
        f.write("    ap_ready : out std_logic;\n")
        f.write("\n")
        f.write("    -- AXI-Stream Input Links \n")
        f.write("    link_in_master : in  LinkMasterArrType(0 to N_INPUT_LINKS-1) := (others => LINK_MASTER_NULL_C);\n")
        f.write("    link_in_slave  : out LinkSlaveArrType(0 to N_INPUT_LINKS-1)  := (others => LINK_SLAVE_NULL_C);\n")
        f.write("\n")
        f.write("    -- AXI-Stream Output Links \n")
        f.write("    link_out_master : out LinkMasterArrType(0 to N_OUTPUT_LINKS-1) := (others => LINK_MASTER_NULL_C);\n")
        f.write("    link_out_slave  : in  LinkSlaveArrType(0 to N_OUTPUT_LINKS-1)  := (others => LINK_SLAVE_NULL_C)\n")
        f.write("    );\n")
        f.write("end algo_top_wrapper;\n")
        f.write("\n")
        f.write("architecture rtl of algo_top_wrapper is\n")
        f.write("  signal ap_rst_n : std_logic;\n")
        f.write("begin\n")
        f.write("\n")
        f.write("  ap_rst_n <= not ap_rst;\n")
        f.write("\n")
        f.write("  algo_top : entity work.algo_top\n")
        f.write("  PORT MAP (\n")
        f.write("    ap_clk => ap_clk,\n")
        f.write("    ap_rst_n => ap_rst_n,\n")
        f.write("    ap_start => ap_start,\n")
        f.write("    ap_done => ap_done,\n")
        f.write("    ap_idle => ap_idle,\n")
        f.write("    ap_ready => ap_ready,\n")
        f.write("\n")

        for i in range(0, hls_input_links):
            f.write("    link_in_" + str(i) + "_TUSER => link_in_master(" + str(i) + ").tUser,\n")
            f.write("    link_in_" + str(i) + "_TDATA => link_in_master(" + str(i) + ").tData,\n")
            f.write("    link_in_" + str(i) + "_TVALID => link_in_master(" + str(i) + ").tValid,\n")
            f.write("    link_in_" + str(i) + "_TLAST(0) => link_in_master(" + str(i) + ").tLast,\n")
            f.write("    link_in_" + str(i) + "_TREADY => link_in_slave(" + str(i) + ").tReady,\n")

        for i in range(0, hls_output_links):
            f.write("    link_out_" + str(i) + "_TUSER => link_out_master(" + str(i) + ").tUser,\n")
            f.write("    link_out_" + str(i) + "_TDATA => link_out_master(" + str(i) + ").tData,\n")
            f.write("    link_out_" + str(i) + "_TVALID => link_out_master(" + str(i) + ").tValid,\n")
            f.write("    link_out_" + str(i) + "_TLAST(0) => link_out_master(" + str(i) + ").tLast,\n")
            if (i == hls_output_links-1): f.write("    link_out_" + str(i) + "_TREADY => link_out_slave(" + str(i) + ").tReady\n")
            else: f.write("    link_out_" + str(i) + "_TREADY => link_out_slave(" + str(i) + ").tReady,\n")

        f.write("  );\n")
        f.write("\n")
        f.write("end rtl;\n")

def main():
    parser = argparse.ArgumentParser(description='HLS-RTL wrapper generator')

    parser.add_argument('header', help='HLS C parameter header file with definitions')
    parser.add_argument('--wrapper', help='Wrapper destination filename and location')

    args = parser.parse_args()
    #print(args)

    hls_input_links = extract_from_header(args.header, "N_INPUT_LINKS")
    hls_output_links = extract_from_header(args.header, "N_OUTPUT_LINKS")

    print("N_INPUT_LINKS = " + str(hls_input_links))
    print("N_OUTPUT_LINKS = " + str(hls_output_links))

    if (args.wrapper != None):
        generate_algo_top_wrapper(args.wrapper, hls_input_links, hls_output_links)

if __name__== "__main__":
	main()