# check_version.py
import pkg_resources
import importlib.util
import inspect
import sys

# Check crewai version
try:
    crewai_version = pkg_resources.get_distribution("crewai").version
    print(f"CrewAI Version: {crewai_version}")
except pkg_resources.DistributionNotFound:
    print("CrewAI is not installed")

# Try to check how tools should be imported
try:
    import crewai
    print("\nAvailable modules in crewai:")
    for module in dir(crewai):
        if not module.startswith("__"):
            print(f"- {module}")
            
    # Check if tools module exists
    if hasattr(crewai, "tools"):
        print("\nContents of crewai.tools:")
        for item in dir(crewai.tools):
            if not item.startswith("__"):
                print(f"- {item}")
                
        # Look for tool-related classes
        if importlib.util.find_spec("crewai.tools.tool"):
            from crewai.tools import tool
            print("\nClasses in crewai.tools.tool:")
            for name, obj in inspect.getmembers(tool):
                if inspect.isclass(obj):
                    print(f"- {name}")
except ImportError as e:
    print(f"Error importing crewai: {e}")

print("\nInstalled packages:")
for package in pkg_resources.working_set:
    if "crew" in package.key or "lang" in package.key:
        print(f"- {package.key}: {package.version}")
        