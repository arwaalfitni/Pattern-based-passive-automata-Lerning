import subprocess
import tempfile
import os


def run_kissat(cnf_path: str,
               system_name: str,
               num_vars: int,
               num_clauses: int):
    """
    Run Kissat on a CNF file.

    Steps:
    1. Prepend:  p cnf <num_vars> <num_clauses>
    2. Run Kissat
    3. Return:
        - "UNSAT"
        - "UNKNOWN"
        - List[int] (model) if SAT
    """

    # Read original content
    with open(cnf_path, "r") as f:
        original_content = f.read()

    # Create a temporary CNF file with header included
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".cnf") as tmp:
        header = f"p cnf {num_vars} {num_clauses}\n"
        tmp.write(header + original_content)
        tmp_cnf_path = tmp.name

    try:
        kissat_path = "kissat"
        # Run Kissat
        result = subprocess.run(
            [kissat_path, tmp_cnf_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        output = result.stdout.splitlines()

        status = None
        model = []

        for line in output:
            line = line.strip()

            if line.startswith("s "):
                # Status line
                if "UNSAT" in line:
                    status = "UNSAT"
                elif "SAT" in line:
                    status = "SAT"
                else:
                    status = "UNKNOWN"

            if line.startswith("v ") and status == "SAT":
                # Model line
                vals = list(map(int, line.split()[1:]))  # remove leading 'v'
                for v in vals:
                    if v != 0:  # kissat ends with 0
                        model.append(v)

        if status == "SAT":
            return model
        else:
            return status

    finally:
        # Clean up temp file
        if os.path.exists(tmp_cnf_path):
            os.remove(tmp_cnf_path)
# Example usage:
# result = run_kissat("/home/arwaalfitni/pycharmProjects/HPCExperimentResult/Random1/longer_training_traces/BiasedSAT/Random1_0_10_BiasedSAT_formula.txt", 826, 33508)
# print(result)

def run_kissat_timeout(cnf_path: str,
               system_name: str,
               num_vars: int,
               num_clauses: int,
               timeout_minutes: int = 5):
    """
    Run Kissat on a CNF file with a timeout.

    Returns:
        - list[int]  -> SAT model (without the ending 0)
        - "UNSAT"
        - "UNKNOWN"
        - "killed"   -> if Kissat exceeded timeout
    """

    timeout_seconds = timeout_minutes * 60  # 15 min → 900 sec

    # Read original content
    with open(cnf_path, "r") as f:
        original_content = f.read()

    # Create a temporary CNF file with header included
    # with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".cnf") as tmp:
    #     header = f"p cnf {num_vars} {num_clauses}\n"
    #     tmp.write(header + original_content)
    #     tmp_cnf_path = tmp.name

    with open(cnf_path, "w") as f:
        header = f"p cnf {num_vars} {num_clauses}\n"
        f.write(header + original_content)
        # tmp_cnf_path = tmp.name
    try:
        kissat_path = "kissat"
        # Run Kissat with timeout
        try:
            result = subprocess.run(
                [kissat_path, cnf_path],#tmp_cnf_path
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=timeout_seconds
            )
        except subprocess.TimeoutExpired:
            # Kissat took more than 5 minutes → kill & return "killed"
            return "TIMEOUT"

        print("Return code:", result.returncode)
        # --------------------------
        # Parse output
        # --------------------------
        output = result.stdout.splitlines()
        # with open(f'{system_name}_SAT_output', "w") as f:
        #     f.write(result.stdout)

        status = None
        model = []

        for line in output:
            line = line.strip()

            if line.startswith("s "):  # status line
                if "UNSAT" in line:
                    status = "UNSAT"
                elif "SAT" in line:
                    status = "SAT"
                else:
                    status = "UNKNOWN"

            if line.startswith("v ") and status == "SAT":
                vals = map(int, line.split()[1:])
                for v in vals:
                    if v != 0:
                        model.append(v)

        if status == "SAT":
            if os.path.exists(cnf_path):
                os.remove(cnf_path)
            return model
        else:
            return status

    finally:
        pass
    #     # Clean up temp file
    #     if os.path.exists(tmp_cnf_path):
    #         os.remove(tmp_cnf_path)

