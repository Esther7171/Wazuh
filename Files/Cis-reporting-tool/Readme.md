## 📄 CIS Report Generator (Wazuh CSV to Word)

This Python script automates the process of converting a **Wazuh CIS benchmark report (CSV format)** into a well-structured **Microsoft Word report (.docx)** using a custom template.

It enables security analysts and auditors to quickly generate client-specific, professional reports with pie chart visualizations and tabulated findings.

### ✨ Features

* 🗂 Loads a Wazuh CIS CSV report (exported from the Wazuh dashboard).
* 🧠 Extracts relevant fields: `Title`, `Result`, and optionally `Rationale`.
* 📊 Generates a pie chart for result distribution.
* 📝 Inserts data into a Word document using a pre-defined template.
* 🧑‍💼 Prompts for the client/agent name to personalize the report.
* ✏️ Optionally allows editing the Word template before report generation.
* 💾 Saves the final `.docx` file to the user's Desktop.

### 🖥 Requirements

* Python 3.8+
* The following Python libraries (install via `pip`):

  ```bash
  pip install pandas matplotlib python-docx
  ```

### 📁 Project Structure

```
/Cis
├── cis.py                     # Main script
├── icon.ico                   # App icon (for executable builds)
├── logo.png                   # Logo (optional, not used directly in code)
├── Report_Template.docx       # Word template to be used for report generation
└── test.py                    # (Optional) Test or helper script
```


### 🚀 Usage

#### 1. Run the Exe

#### 2. Select the **Wazuh-exported CSV file** when prompted.
#### 3. Enter the **Agent/Client name**.
#### 4. Choose whether to edit the Word template before generating the report.

#### 5. Output

* A `.docx` report will be generated and saved to your **Desktop**, named:

  ```
  <AgentName>-<YYYY-MM-DD>-assessment-report.docx
  ```

### 📊 CSV Format Requirements

Your CSV should include at least the following columns:

* `Title` – The name of the CIS item or setting.
* `Result` – Pass/Fail status.
* `Rationale` *(optional)* – The reasoning or justification.

The script will normalize column names and fill missing `Rationale` with "N/A" automatically.

