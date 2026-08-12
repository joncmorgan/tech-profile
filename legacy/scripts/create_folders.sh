#!/bin/bash

# Explicitly set your exact local Nextcloud folder path
NEXTCLOUD_DIR="$HOME/Nextdrive/jonmorgan.au"

# Verify the target sync directory exists on your file system
if [ ! -d "$NEXTCLOUD_DIR" ]; then
    echo "❌ Error: Could not find directory at: $NEXTCLOUD_DIR"
    echo "Please make sure your Nextcloud storage folder name matches exactly."
    exit 1
fi

CONSULTING_DIR="$NEXTCLOUD_DIR/Consulting"
TEMPLATE_DIR="$CONSULTING_DIR/.client_template"

# 1. Ensure the base template folders exist locally
mkdir -p "$TEMPLATE_DIR/01_Engagement_&_Admin/Proposals_&_Quotes"
mkdir -p "$TEMPLATE_DIR/01_Engagement_&_Admin/SOW_&_Contracts"
mkdir -p "$TEMPLATE_DIR/01_Engagement_&_Admin/Invoices_&_PO"
mkdir -p "$TEMPLATE_DIR/🗂️_Project_Name_A/01_Admin_&_Scope"
mkdir -p "$TEMPLATE_DIR/🗂️_Project_Name_A/02_Incoming_Info"
mkdir -p "$TEMPLATE_DIR/🗂️_Project_Name_A/03_Work_In_Progress"
mkdir -p "$TEMPLATE_DIR/🗂️_Project_Name_A/04_Outgoing_Deliverables"
mkdir -p "$TEMPLATE_DIR/🗂️_Project_Name_A/05_Meeting_Minutes"
mkdir -p "$CONSULTING_DIR/🗄️_Internal_Operations/Templates_&_Assets"
mkdir -p "$CONSULTING_DIR/🗄️_Internal_Operations/Finances_&_Tax"

# 2. Collect client configuration parameter
echo "=================================================="
read -p "🏢 Enter the new Client Name (e.g., Deloitte): " CLIENT_NAME
echo "=================================================="

if [ -z "$CLIENT_NAME" ]; then
    echo "❌ Client name cannot be blank."
    exit 1
fi

TARGET_DIR="$CONSULTING_DIR/$CLIENT_NAME"

# Check if client folder already exists
if [ -d "$TARGET_DIR" ]; then
    echo "⚠️  A folder named '$CLIENT_NAME' already exists in your Consulting directory!"
    exit 1
fi

# 3. Print deployment structural summary
echo ""
echo "📋 PROPOSED DEPLOYMENT SUMMARY"
echo "--------------------------------------------------"
echo "Local Path: $TARGET_DIR/"
echo ""
echo "Structures to be generated:"
echo " ├── 01_Engagement_&_Admin/"
echo " │   ├── Proposals_&_Quotes/"
echo " │   ├── SOW_&_Contracts/"
echo " │   └── Invoices_&_PO/"
echo " └── 🗂️_Project_Name_A/"
echo "     ├── 01_Admin_&_Scope/"
echo "     ├── 02_Incoming_Info/"
echo "     ├── 03_Work_In_Progress/"
echo "     ├── 04_Outgoing_Deliverables/"
echo "     └── 05_Meeting_Minutes/"
echo "--------------------------------------------------"
echo ""

read -p "❓ Proceed with creating this directory matrix? (y/N): " CONFIRM

CONFIRM=$(echo "$CONFIRM" | tr '[:upper:]' '[:lower:]')

if [[ "$CONFIRM" == "y" || "$CONFIRM" == "yes" ]]; then
    echo ""
    echo "🚀 Instantly writing directory matrix for '$CLIENT_NAME'..."
    cp -r "$TEMPLATE_DIR" "$TARGET_DIR"
    echo "✓ Success! Framework built at target path. Syncing to the cloud now."
else
    echo ""
    echo "❌ Operation cancelled. No directories were created."
fi
echo ""