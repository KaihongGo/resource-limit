import subprocess
import resource
import os
import sys
import signal

# Define the CPU limit (in seconds) for comparison
CPU_LIMIT = 20
# Set the maximum address space (virtual memory) to 512MB (512 * 1024 * 1024 bytes)
MEM_LIMIT = 512 * 1024 * 1024
# Set a timeout for the subprocess (in seconds)
SUBPROCESS_TIMEOUT = 2 * CPU_LIMIT

def set_limits():
    try:
        soft_mem, hard_mem = MEM_LIMIT, MEM_LIMIT
        resource.setrlimit(resource.RLIMIT_AS, (soft_mem, hard_mem))

        # Set the CPU time limit to 20 seconds
        soft_cpu, hard_cpu = CPU_LIMIT, CPU_LIMIT  # in seconds
        resource.setrlimit(resource.RLIMIT_CPU, (soft_cpu, hard_cpu))
    except ValueError as e:
        print(f"Error setting resource limits: {e}")
    except resource.error as e:
        print(f"Resource limit error: {e}")
    except Exception as e:
        print(f"Unexpected error while setting limits: {e}")

def print_resource_usage():
    try:
        usage = resource.getrusage(resource.RUSAGE_CHILDREN)

        print("\nResource usage of the subprocess:")
        print(f"User time: {usage.ru_utime:.2f} seconds")
        print(f"System time: {usage.ru_stime:.2f} seconds")
        print(f"Total CPU time: {usage.ru_utime + usage.ru_stime:.2f} seconds")
        print(f"Max memory usage: {usage.ru_maxrss} KB")
        print(f"Shared memory size: {usage.ru_ixrss} KB")
        print(f"Unshared memory size: {usage.ru_idrss} KB")
        print(f"Unshared stack size: {usage.ru_isrss} KB")
        print(f"Page faults not requiring I/O: {usage.ru_minflt}")
        print(f"Page faults requiring I/O: {usage.ru_majflt}")
        print(f"Number of swap outs: {usage.ru_nswap}")
        print(f"Block input operations: {usage.ru_inblock}")
        print(f"Block output operations: {usage.ru_oublock}")
        print(f"Messages sent: {usage.ru_msgsnd}")
        print(f"Messages received: {usage.ru_msgrcv}")
        print(f"Signals received: {usage.ru_nsignals}")
        print(f"Voluntary context switches: {usage.ru_nvcsw}")
        print(f"Involuntary context switches: {usage.ru_nivcsw}")

        # Check if the total CPU time used exceeds the set limit
        total_cpu_time = usage.ru_utime + usage.ru_stime
        if total_cpu_time >= CPU_LIMIT:
            print(f"WARNING: The subprocess reached or exceeded the CPU time limit of {CPU_LIMIT} seconds.")
    except resource.error as e:
        print(f"Resource usage error: {e}")
    except Exception as e:
        print(f"Unexpected error while printing resource usage: {e}")

def run_subprocess():
    try:
        # Set the memory and CPU time limits before starting the subprocess
        set_limits()

        # Run the C++ subprocess with a timeout
        result = subprocess.run(["./your_cpp_program"], check=True, timeout=SUBPROCESS_TIMEOUT)

        # Check the result (you can check the return code or output here)
        print("Subprocess finished successfully.")

    except subprocess.TimeoutExpired:
        print(f"Subprocess timed out after {SUBPROCESS_TIMEOUT} seconds!")
    except subprocess.CalledProcessError as e:
        print(f"Subprocess returned non-zero exit status: {e.returncode}")
    except MemoryError:
        print("Memory limit exceeded!")
    except FileNotFoundError:
        print("The executable ./your_cpp_program was not found.")
    except PermissionError:
        print("Permission denied while trying to execute ./your_cpp_program.")
    except OSError as e:
        print(f"OS error occurred: {e}")
    except KeyboardInterrupt:
        print("Execution was interrupted by the user.")
    except resource.error as e:
        print(f"Resource limit error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        # Print resource usage after the subprocess has finished
        print_resource_usage()

if __name__ == "__main__":
    try:
        run_subprocess()
    except Exception as e:
        print(f"An error occurred during execution: {e}")
    finally:
        print("Script execution completed.")
