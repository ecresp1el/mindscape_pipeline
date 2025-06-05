#!/usr/bin/env bash
# run_pipeline.sh
# Description: Launch MindScape Snakemake pipeline using a shared Turbo project directory.

set -euo pipefail

#########################################
# CONFIGURATION
#########################################
CONFIG_FILE="config/config.yaml"
SNAKEFILE="workflow/Snakefile"

#########################################
# STEP 1: Inform user and run create_project
#########################################
echo "🚀 Launching MindScape pipeline setup..."
echo "📦 Creating project structure..."

snakemake --snakefile "$SNAKEFILE" \
          --configfile "$CONFIG_FILE" \
          --cores 1 \
          --printshellcmds \
          --rerun-incomplete \
          create_project

#########################################
# STEP 2: Extract project_path from updated config
#########################################
PROJECT_PATH=$(python -c "import yaml; print(yaml.safe_load(open('$CONFIG_FILE'))['project_path'])")
UPDATED_CONFIG="$PROJECT_PATH/config/config.yaml"

echo "✅ Project directory created at: $PROJECT_PATH"

#########################################
# STEP 3: Run remaining workflow steps from inside project
#########################################
echo "🔁 Running remaining workflow steps..."
cd "$PROJECT_PATH"

snakemake --snakefile "$OLDPWD/$SNAKEFILE" \
          --configfile "$UPDATED_CONFIG" \
          --cores 1 \
          --printshellcmds \
          --rerun-incomplete