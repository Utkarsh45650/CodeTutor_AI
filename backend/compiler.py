from flask import Blueprint, request, jsonify
from auth import token_required
import subprocess
import tempfile
import os
import sys

compiler_bp = Blueprint('compiler', __name__)

@compiler_bp.route('/run_code', methods=['POST'])
@token_required
def run_code(current_user):
    data = request.get_json()
    code = data.get('code', '')
    language = data.get('language', '').lower()
    
    if not code or not language:
        return jsonify({'error': 'Code and language are required'}), 400
    
    try:
        if language == 'python':
            return run_python_code(code)
        elif language == 'c':
            return run_c_code(code)
        elif language == 'c++' or language == 'cpp':
            return run_cpp_code(code)
        elif language == 'java':
            return run_java_code(code)
        elif language == 'c#' or language == 'csharp':
            return run_csharp_code(code)
        else:
            return jsonify({'error': f'Language {language} not supported'}), 400
    
    except Exception as e:
        return jsonify({
            'success': False,
            'output': '',
            'error': f'Execution error: {str(e)}'
        }), 500

def run_python_code(code):
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            f.flush()
            
            # Run the Python code
            result = subprocess.run(
                [sys.executable, f.name],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            os.unlink(f.name)
            
            return jsonify({
                'success': result.returncode == 0,
                'output': result.stdout,
                'error': result.stderr if result.stderr else None
            })
    
    except subprocess.TimeoutExpired:
        return jsonify({
            'success': False,
            'output': '',
            'error': 'Code execution timed out (10 seconds limit)'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'output': '',
            'error': f'Python execution error: {str(e)}'
        })

def run_c_code(code):
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            source_file = os.path.join(temp_dir, 'program.c')
            executable_file = os.path.join(temp_dir, 'program.exe')
            
            # Write source code
            with open(source_file, 'w') as f:
                f.write(code)
            
            # Compile
            compile_result = subprocess.run(
                ['gcc', source_file, '-o', executable_file],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if compile_result.returncode != 0:
                return jsonify({
                    'success': False,
                    'output': '',
                    'error': f'Compilation error: {compile_result.stderr}'
                })
            
            # Run
            run_result = subprocess.run(
                [executable_file],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            return jsonify({
                'success': run_result.returncode == 0,
                'output': run_result.stdout,
                'error': run_result.stderr if run_result.stderr else None
            })
    
    except subprocess.TimeoutExpired:
        return jsonify({
            'success': False,
            'output': '',
            'error': 'Code execution timed out'
        })
    except FileNotFoundError:
        return jsonify({
            'success': False,
            'output': '',
            'error': 'GCC compiler not found. Please install GCC to run C code.'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'output': '',
            'error': f'C execution error: {str(e)}'
        })

def run_cpp_code(code):
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            source_file = os.path.join(temp_dir, 'program.cpp')
            executable_file = os.path.join(temp_dir, 'program.exe')
            
            # Write source code
            with open(source_file, 'w') as f:
                f.write(code)
            
            # Compile
            compile_result = subprocess.run(
                ['g++', source_file, '-o', executable_file],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if compile_result.returncode != 0:
                return jsonify({
                    'success': False,
                    'output': '',
                    'error': f'Compilation error: {compile_result.stderr}'
                })
            
            # Run
            run_result = subprocess.run(
                [executable_file],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            return jsonify({
                'success': run_result.returncode == 0,
                'output': run_result.stdout,
                'error': run_result.stderr if run_result.stderr else None
            })
    
    except subprocess.TimeoutExpired:
        return jsonify({
            'success': False,
            'output': '',
            'error': 'Code execution timed out'
        })
    except FileNotFoundError:
        return jsonify({
            'success': False,
            'output': '',
            'error': 'G++ compiler not found. Please install G++ to run C++ code.'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'output': '',
            'error': f'C++ execution error: {str(e)}'
        })

def run_java_code(code):
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            # Extract class name from code (simple approach)
            class_name = 'Main'
            lines = code.split('\n')
            for line in lines:
                if 'public class' in line:
                    parts = line.split()
                    if len(parts) >= 3:
                        class_name = parts[2]
                    break
            
            source_file = os.path.join(temp_dir, f'{class_name}.java')
            
            # Write source code
            with open(source_file, 'w') as f:
                f.write(code)
            
            # Compile
            compile_result = subprocess.run(
                ['javac', source_file],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=temp_dir
            )
            
            if compile_result.returncode != 0:
                return jsonify({
                    'success': False,
                    'output': '',
                    'error': f'Compilation error: {compile_result.stderr}'
                })
            
            # Run
            run_result = subprocess.run(
                ['java', class_name],
                capture_output=True,
                text=True,
                timeout=10,
                cwd=temp_dir
            )
            
            return jsonify({
                'success': run_result.returncode == 0,
                'output': run_result.stdout,
                'error': run_result.stderr if run_result.stderr else None
            })
    
    except subprocess.TimeoutExpired:
        return jsonify({
            'success': False,
            'output': '',
            'error': 'Code execution timed out'
        })
    except FileNotFoundError:
        return jsonify({
            'success': False,
            'output': '',
            'error': 'Java compiler not found. Please install JDK to run Java code.'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'output': '',
            'error': f'Java execution error: {str(e)}'
        })

def run_csharp_code(code):
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            source_file = os.path.join(temp_dir, 'program.cs')
            
            # Write source code
            with open(source_file, 'w') as f:
                f.write(code)
            
            # Try to compile and run with dotnet
            try:
                # Create a minimal project file
                csproj_content = '''<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>net6.0</TargetFramework>
  </PropertyGroup>
</Project>'''
                
                csproj_file = os.path.join(temp_dir, 'program.csproj')
                with open(csproj_file, 'w') as f:
                    f.write(csproj_content)
                
                # Run with dotnet
                run_result = subprocess.run(
                    ['dotnet', 'run'],
                    capture_output=True,
                    text=True,
                    timeout=30,
                    cwd=temp_dir
                )
                
                return jsonify({
                    'success': run_result.returncode == 0,
                    'output': run_result.stdout,
                    'error': run_result.stderr if run_result.stderr else None
                })
                
            except FileNotFoundError:
                return jsonify({
                    'success': False,
                    'output': '',
                    'error': '.NET SDK not found. Please install .NET SDK to run C# code.'
                })
    
    except subprocess.TimeoutExpired:
        return jsonify({
            'success': False,
            'output': '',
            'error': 'Code execution timed out'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'output': '',
            'error': f'C# execution error: {str(e)}'
        })
