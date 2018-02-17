find . -name "__pycache__" -exec rm -rf {} \;
find . -name ".cache" -exec rm -rf {} \;
find . -name ".DS_Store" -exec rm -rf {} \;
find . -name "*.pyc" -delete
find . -name "*.swo" -exec rm -rf {} \;
find . -name "*.swp" -exec rm -rf {} \;
echo "Success: Python caches and vim relics have been deleted."

