import subprocess
import resource
import os
import sys

def set_memory_limit():
    # Set the maximum address space (virtual memory) to 512MB (512 * 1024 * 1024 bytes)
    soft, hard = 512 * 1024 * 1024, 512 * 1024 * 1024
    resource.setrlimit(resource.RLIMIT_AS, (soft, hard))

def print_resource_usage():
    usage = resource.getrusage(resource.RUSAGE_CHILDREN)
    print("\nResource usage of the subprocess:")
    print(f"User time: {usage.ru_utime} seconds")
    print(f"System time: {usage.ru_stime} seconds")
    print(f"Max memory usage: {usage.ru_maxrss} KB")
    print(f"Input blocks: {usage.ru_inblock}")
    print(f"Output blocks: {usage.ru_oublock}")
    print(f"Voluntary context switches: {usage.ru_nvcsw}")
    print(f"Involuntary context switches: {usage.ru_nivcsw}")

def run_subprocess():
    try:
        # Set the memory limit before starting the subprocess
        set_memory_limit()

        # Define the time limit (in seconds)
        time_limit = 10  # for example, 2 seconds

        # Run the C++ subprocess with a time limit
        result = subprocess.run(["./your_cpp_program"], check=True, timeout=time_limit)

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
