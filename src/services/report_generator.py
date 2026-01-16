from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
import os

class PDFReportGenerator:
    def __init__(self):
        self.reports_dir = 'reports'
        os.makedirs(self.reports_dir, exist_ok=True)
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Setup custom paragraph styles"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2563eb'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#1e40af'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
    
    def generate_report(self, assessment_id, username, prediction):
        """Generate PDF report for genetic risk assessment"""
        # Debug logging
        print(f"DEBUG REPORT: Received username parameter: '{username}' (type: {type(username)})")
        
        # Handle empty or None username
        if not username or username.strip() == '' or username == 'Guest':
            display_name = 'Not Provided'
            safe_username = 'Guest'
        else:
            display_name = username.strip()
            # Sanitize username for filename
            safe_username = ''.join(c for c in username if c.isalnum() or c in (' ', '_')).strip()
            safe_username = safe_username.replace(' ', '_')[:30]  # Limit length
            if not safe_username:  # If sanitization removed everything
                safe_username = 'Patient'
        
        print(f"DEBUG REPORT: Display name: '{display_name}', Safe username: '{safe_username}'")
        
        filename = f"GeneticReport_{safe_username}_{assessment_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(self.reports_dir, filename)
        
        doc = SimpleDocTemplate(filepath, pagesize=letter,
                              rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=18)
        
        story = []
        
        # Title
        title = Paragraph("GeneAccessAI<br/>Genetic Risk Assessment Report", 
                         self.styles['CustomTitle'])
        story.append(title)
        story.append(Spacer(1, 0.3*inch))
        
        # Patient Information
        story.append(Paragraph("Patient Information", self.styles['SectionHeader']))
        patient_data = [
            ['Patient Name:', display_name],
            ['Report ID:', f'GA-{assessment_id:06d}'],
            ['Assessment Date:', datetime.now().strftime('%B %d, %Y')],
            ['Report Time:', datetime.now().strftime('%I:%M %p')],
            ['Report Generated:', datetime.now().strftime('%B %d, %Y at %I:%M %p')]
        ]
        patient_table = Table(patient_data, colWidths=[2.2*inch, 3.8*inch])
        patient_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e0e7ff')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
        ]))
        story.append(patient_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Risk Assessment Results
        story.append(Paragraph("Risk Assessment Results", self.styles['SectionHeader']))
        
        risk_color = self.get_risk_color(prediction['risk_level'])
        results_data = [
            ['Predicted Condition:', prediction['disorder']],
            ['Risk Score:', f"{prediction['risk_score']}%"],
            ['Risk Level:', prediction['risk_level']],
            ['Confidence:', f"{prediction['confidence']}%"]
        ]
        results_table = Table(results_data, colWidths=[2*inch, 4*inch])
        results_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#dbeafe')),
            ('BACKGROUND', (1, 2), (1, 2), risk_color),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        story.append(results_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Recommendations
        story.append(Paragraph("Medical Recommendations", self.styles['SectionHeader']))
        for i, rec in enumerate(prediction['recommendations'], 1):
            rec_text = Paragraph(f"{i}. {rec}", self.styles['BodyText'])
            story.append(rec_text)
            story.append(Spacer(1, 0.1*inch))
        
        story.append(Spacer(1, 0.3*inch))
        
        # Disclaimer
        story.append(Paragraph("Important Disclaimer", self.styles['SectionHeader']))
        disclaimer_text = """
        This report is generated by an AI-powered system and is intended for informational 
        purposes only. It should NOT be used as a substitute for professional medical advice, 
        diagnosis, or treatment. Always seek the advice of your physician or other qualified 
        health provider with any questions you may have regarding a medical condition. 
        Genetic testing and counseling with certified professionals is recommended for 
        accurate diagnosis.
        """
        disclaimer = Paragraph(disclaimer_text, self.styles['BodyText'])
        story.append(disclaimer)
        
        # Footer
        story.append(Spacer(1, 0.5*inch))
        footer_text = Paragraph(
            "GeneAccessAI - AI-Powered Genetic Health Platform<br/>www.geneaccessai.com",
            ParagraphStyle('Footer', parent=self.styles['Normal'], 
                          fontSize=9, textColor=colors.grey, alignment=TA_CENTER)
        )
        story.append(footer_text)
        
        # Build PDF
        doc.build(story)
        return filepath
    
    def get_risk_color(self, risk_level):
        """Get color based on risk level"""
        colors_map = {
            'Low': colors.HexColor('#86efac'),
            'Moderate': colors.HexColor('#fde047'),
            'High': colors.HexColor('#fca5a5')
        }
        return colors_map.get(risk_level, colors.white)
