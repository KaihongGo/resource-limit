import subprocess
import resource
import os
import sys

def set_limits():
    # Set the maximum address space (virtual memory) to 512MB (512 * 1024 * 1024 bytes)
    soft_mem, hard_mem = 512 * 1024 * 1024, 512 * 1024 * 1024
    resource.setrlimit(resource.RLIMIT_AS, (soft_mem, hard_mem))

    # Set the CPU time limit to 2 seconds
    soft_cpu, hard_cpu = 2, 2  # in seconds
    resource.setrlimit(resource.RLIMIT_CPU, (soft_cpu, hard_cpu))

import resource

def print_resource_usage():
    usage = resource.getrusage(resource.RUSAGE_CHILDREN)
    
    print("\nResource usage of the subprocess:")
    print(f"User time: {usage.ru_utime:.2f} seconds")
    print(f"System time: {usage.ru_stime:.2f} seconds")
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

def run_subprocess():
    try:
        # Set the memory and CPU time limits before starting the subprocess
        set_limits()

        # Run the C++ subprocess without specifying a timeout in subprocess.run
        result = subprocess.run(["./your_cpp_program"], check=True)

        # Check the result (you can check the return code or output here)
        print("Subprocess finished successfully.")

    except subprocess.TimeoutExpired:
        print("Subprocess timed out!")
    except subprocess.CalledProcessError as e:
        print(f"Subprocess returned non-zero exit status: {e.returncode}")
    except MemoryError:
        print("Memory limit exceeded!")
    finally:
        # Print resource usage after the subprocess has finished
        print_resource_usage()

if __name__ == "__main__":
    run_subprocess()
