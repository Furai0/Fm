import subprocess
import os
import sys

script_to_run = os.getcwd()

def run_python_script_in_xterm(script_path):
    try:
        command = [
            'xterm',
            '-geometry', '155x50+100+100',
            '-T', 'FM',
            '-e',
            f'{sys.executable} {script_path}'
        ]
        
        process = subprocess.Popen(
            ' '.join(command),
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        return process
    except Exception as e:
        print(f"Ошибка при запуске скрипта: {e}")
        return None


if __name__ == "__main__":

    script_to_run = f"{script_to_run}/nah.py"
    
    if not os.path.exists(script_to_run):
        print(f"Файл {script_to_run} не найден!")
        sys.exit(1)
    
    process = run_python_script_in_xterm(script_to_run)

