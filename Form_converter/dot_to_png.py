# import subprocess
#
# def dot_to_png(dot_filename, png_filename="output.png"):
#     try:
#         subprocess.run(['dot', '-Tpng', dot_filename, '-o', png_filename], check=True)
#         print(f"PNG file generated: {png_filename}")
#     except subprocess.CalledProcessError as e:
#         print("Error generating PNG:", e)

import subprocess
import os



def dot_to_png(dot_filename, png_filename="output.png"):
    if not os.path.isfile(dot_filename):
        print(f"DOT file not found: {dot_filename}")
        return
    try:
        subprocess.run(['dot', '-Tpng', dot_filename, '-o', png_filename], check=True)
        print(f"PNG file generated: {png_filename}")
    except subprocess.CalledProcessError as e:
        print("Error generating PNG:", e)

#usage example
if __name__ == "__main__":
    dot_to_png("/home/arwaalfitni/pycharmProjects/HPCExperimentResult/PositiveOnly_minimumCoverage_shortTraces/coffeemachine/TransitionCover/DFASAT/coffeemachine_1_200_DFASAT.dot",
               "coffeemachine_1_200_DFASAT.png")
    dot_to_png(
        "/home/arwaalfitni/pycharmProjects/HPCExperimentResult/PositiveOnly_minimumCoverage_shortTraces/coffeemachine/TransitionCover/BiasedEDSM1/coffeemachine_1_200_BiasedEDSM.dot",
        "coffeemachine_1_200_BiasedEDSM1.png")

    #
    # dot_to_png("../TextEditorPaper/TransitionCover/BiasedSAT1/TextEditorPaper_0_3_BiasedSAT1.dot",
    #            "../TextEditorPaper/TransitionCover/BiasedSAT1/TextEditorPaper_0_3_BiasedSAT1.png")
    #
    # dot_to_png("../TextEditorPaper/TransitionCover/BiasedEDSM1/TextEditorPaper_0_3_BiasedEDSM1.dot",
    #            "../TextEditorPaper/TransitionCover/BiasedEDSM1/TextEditorPaper_0_3_BiasedEDSM1.png")
    # dot_to_png("../TextEditorPaper/TransitionCover/DFASAT/TextEditorPaper_0_3_DFASAT.dot",
    #             "../TextEditorPaper/TransitionCover/DFASAT/TextEditorPaper_0_3_DFASAT.png")

# dot_to_png("../reference_automata/Random3_reference.dot",
    #            "../reference_automata/Random3_reference.png")
    # dot_to_png("../reference_automata/coffeemachine_reference.dot",
    #            "../reference_automata/coffeemachine_reference.png")