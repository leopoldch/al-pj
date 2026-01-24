import sys
import xml.etree.ElementTree as ET
from fpdf import FPDF
from datetime import datetime

class TestReportPDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 20)
        self.cell(0, 10, 'Test Execution Report', new_x="LMARGIN", new_y="NEXT", align='C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

def generate_report(xml_file, output_file):
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        if root.tag == 'testsuites':
            root = root[0]
            
        name = root.get('name', 'Backend Tests')
        tests = int(root.get('tests', 0))
        failures = int(root.get('failures', 0))
        errors = int(root.get('errors', 0))
        skipped = int(root.get('skipped', 0))
        time_taken = float(root.get('time', 0.0))
        timestamp = root.get('timestamp', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        passed = tests - failures - errors - skipped
        pass_rate = (passed / tests * 100) if tests > 0 else 0

        pdf = TestReportPDF()
        pdf.add_page()
        
        pdf.set_font('Helvetica', 'B', 16)
        pdf.cell(0, 10, 'Summary', new_x="LMARGIN", new_y="NEXT")
        pdf.ln(5)
        
        pdf.set_font('Helvetica', '', 12)
        pdf.cell(50, 10, f'Timestamp: {timestamp}', new_x="LMARGIN", new_y="NEXT")
        pdf.cell(50, 10, f'Total Time: {time_taken:.2f}s', new_x="LMARGIN", new_y="NEXT")
        pdf.ln(5)
        
        pdf.set_font('Helvetica', 'B', 12)
        pdf.set_fill_color(240, 240, 240)
        pdf.cell(40, 10, 'Total', border=1, fill=True)
        pdf.cell(40, 10, str(tests), border=1, new_x="LMARGIN", new_y="NEXT")
        
        pdf.set_text_color(0, 128, 0)
        pdf.cell(40, 10, 'Passed', border=1, fill=True)
        pdf.cell(40, 10, f'{passed} ({pass_rate:.1f}%)', border=1, new_x="LMARGIN", new_y="NEXT")
        
        pdf.set_text_color(255, 0, 0)
        pdf.cell(40, 10, 'Failures/Errors', border=1, fill=True)
        pdf.cell(40, 10, str(failures + errors), border=1, new_x="LMARGIN", new_y="NEXT")
        
        pdf.set_text_color(255, 165, 0)
        pdf.cell(40, 10, 'Skipped', border=1, fill=True)
        pdf.cell(40, 10, str(skipped), border=1, new_x="LMARGIN", new_y="NEXT")
        
        pdf.set_text_color(0, 0, 0)
        pdf.ln(10)

        pdf.add_page()
        pdf.set_font('Helvetica', 'B', 16)
        pdf.cell(0, 10, 'Test Details', new_x="LMARGIN", new_y="NEXT")
        pdf.ln(5)

        pdf.set_font('Helvetica', 'B', 10)
        pdf.set_fill_color(200, 200, 200)
        pdf.cell(120, 10, 'Test Case', border=1, fill=True)
        pdf.cell(30, 10, 'Status', border=1, fill=True)
        pdf.cell(30, 10, 'Time (s)', border=1, fill=True, new_x="LMARGIN", new_y="NEXT")

        pdf.set_font('Helvetica', '', 9)

        for testcase in root.findall('.//testcase'):
            classname = testcase.get('classname')
            testcase_name = testcase.get('name')
            time_val = float(testcase.get('time', 0.0))
            full_name = f"{classname}.{testcase_name}"
            
            status = 'PASSED'
            pdf.set_text_color(0, 128, 0)
            
            if testcase.find('failure') is not None:
                status = 'FAILED'
                pdf.set_text_color(255, 0, 0)
            elif testcase.find('error') is not None:
                status = 'ERROR'
                pdf.set_text_color(255, 0, 0)
            elif testcase.find('skipped') is not None:
                status = 'SKIPPED'
                pdf.set_text_color(255, 165, 0)
            
            display_name = (full_name[:75] + '..') if len(full_name) > 75 else full_name
            
            pdf.cell(120, 8, display_name, border=1)
            pdf.cell(30, 8, status, border=1)
            pdf.set_text_color(0, 0, 0)
            pdf.cell(30, 8, f"{time_val:.4f}", border=1, new_x="LMARGIN", new_y="NEXT")

        if failures > 0 or errors > 0:
            pdf.set_font('Helvetica', 'B', 16)
            pdf.cell(0, 10, 'Failure Details', new_x="LMARGIN", new_y="NEXT")
            pdf.ln(5)
            
            pdf.set_font('Helvetica', '', 10)
            for testcase in root.findall('testcase'):
                failure = testcase.find('failure')
                error = testcase.find('error')
                
                if failure is not None or error is not None:
                    classname = testcase.get('classname')
                    testcase_name = testcase.get('name')
                    message = (failure.get('message') if failure is not None else error.get('message')) or "No message"
                    
                    pdf.set_text_color(255, 0, 0)
                    pdf.cell(0, 8, f'FAIL: {classname}.{testcase_name}', new_x="LMARGIN", new_y="NEXT")
                    pdf.set_text_color(0, 0, 0)
                    pdf.multi_cell(0, 5, f'Message: {message[:300]}...')
                    pdf.ln(3)

        pdf.output(output_file)
        print(f"Report generated: {output_file}")
        
    except Exception as e:
        print(f"Error generating PDF: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python generate_pdf_report.py <input_xml> <output_pdf>")
        sys.exit(1)
        
    generate_report(sys.argv[1], sys.argv[2])
