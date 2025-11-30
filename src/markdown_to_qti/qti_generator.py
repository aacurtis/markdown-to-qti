"""
QTI 1.2 XML generator for Canvas LMS import.

Note: Canvas LMS uses QTI 1.2 format (compatible with IMS QTI specification).
"""
import html
import re
import uuid
import zipfile
from pathlib import Path
from typing import List
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

from .parser import Question


def _generate_identifier() -> str:
    """Generate a unique identifier for QTI elements."""
    return f"g{uuid.uuid4().hex[:24]}"


def _markdown_to_html(text: str) -> str:
    """
    Convert markdown text with code blocks to HTML.
    
    Args:
        text: Markdown text that may contain code blocks.
        
    Returns:
        HTML formatted text.
    """
    # First, escape HTML in the text but preserve code blocks
    code_block_pattern = r'```(\w*)\n(.*?)```'
    
    # Find all code blocks and replace with placeholders
    code_blocks = []
    
    def save_code_block(match):
        lang = match.group(1) or ''
        code = match.group(2)
        placeholder = f"__CODE_BLOCK_{len(code_blocks)}__"
        code_blocks.append((lang, code))
        return placeholder
    
    text_with_placeholders = re.sub(code_block_pattern, save_code_block, text, flags=re.DOTALL)
    
    # Escape HTML in the remaining text
    escaped_text = html.escape(text_with_placeholders)
    
    # Convert newlines to <br/> tags (except before/after code blocks)
    escaped_text = escaped_text.replace('\n', '<br/>\n')
    
    # Handle inline code
    escaped_text = re.sub(r'`([^`]+)`', r'<code>\1</code>', escaped_text)
    
    # Restore code blocks as HTML
    for i, (lang, code) in enumerate(code_blocks):
        placeholder = f"__CODE_BLOCK_{i}__"
        escaped_code = html.escape(code.rstrip())
        if lang:
            html_code = f'<pre><code class="language-{lang}">{escaped_code}</code></pre>'
        else:
            html_code = f'<pre><code>{escaped_code}</code></pre>'
        escaped_text = escaped_text.replace(placeholder, html_code)
    
    return escaped_text


def generate_qti_manifest(assessment_id: str, title: str) -> str:
    """
    Generate the imsmanifest.xml content for the QTI package.
    
    Args:
        assessment_id: Unique identifier for the assessment.
        title: Title of the assessment.
        
    Returns:
        XML string for the manifest.
    """
    manifest = Element('manifest')
    manifest.set('identifier', f"manifest_{assessment_id}")
    manifest.set('xmlns', 'http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1')
    manifest.set('xmlns:lom', 'http://ltsc.ieee.org/xsd/imsccv1p1/LOM/resource')
    manifest.set('xmlns:imsmd', 'http://www.imsglobal.org/xsd/imsmd_v1p2')
    manifest.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    
    # Metadata
    metadata = SubElement(manifest, 'metadata')
    schema = SubElement(metadata, 'schema')
    schema.text = 'IMS Content'
    schemaversion = SubElement(metadata, 'schemaversion')
    schemaversion.text = '1.1.3'
    
    # Organizations (empty for QTI)
    SubElement(manifest, 'organizations')
    
    # Resources
    resources = SubElement(manifest, 'resources')
    resource = SubElement(resources, 'resource')
    resource.set('identifier', assessment_id)
    resource.set('type', 'imsqti_xmlv1p2')
    resource.set('href', f"{assessment_id}/{assessment_id}.xml")
    
    file_elem = SubElement(resource, 'file')
    file_elem.set('href', f"{assessment_id}/{assessment_id}.xml")
    
    # Pretty print
    xml_str = tostring(manifest, encoding='unicode')
    return minidom.parseString(xml_str).toprettyxml(indent="  ")


def generate_qti_assessment(
    questions: List[Question],
    title: str = "Assessment",
    assessment_id: str = None
) -> str:
    """
    Generate QTI 2.2 compatible XML for Canvas LMS.
    
    Args:
        questions: List of Question objects to convert.
        title: Title of the assessment.
        assessment_id: Unique identifier for the assessment.
        
    Returns:
        QTI XML string.
    """
    if assessment_id is None:
        assessment_id = _generate_identifier()
    
    # Root element - using QTI 1.2 format which Canvas accepts
    questestinterop = Element('questestinterop')
    questestinterop.set('xmlns', 'http://www.imsglobal.org/xsd/ims_qtiasiv1p2')
    questestinterop.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    questestinterop.set('xsi:schemaLocation', 
        'http://www.imsglobal.org/xsd/ims_qtiasiv1p2 http://www.imsglobal.org/xsd/ims_qtiasiv1p2p1.xsd')
    
    # Assessment element
    assessment = SubElement(questestinterop, 'assessment')
    assessment.set('ident', assessment_id)
    assessment.set('title', title)
    
    # Assessment metadata
    qtimetadata = SubElement(assessment, 'qtimetadata')
    _add_metadata_field(qtimetadata, 'qmd_timelimit', '')
    _add_metadata_field(qtimetadata, 'cc_maxattempts', '1')
    
    # Section containing all items
    section = SubElement(assessment, 'section')
    section.set('ident', 'root_section')
    
    # Add each question as an item
    for question in questions:
        item = _create_question_item(question)
        section.append(item)
    
    # Pretty print
    xml_str = tostring(questestinterop, encoding='unicode')
    return minidom.parseString(xml_str).toprettyxml(indent="  ")


def _add_metadata_field(parent: Element, label: str, value: str):
    """Add a metadata field to the parent element."""
    field = SubElement(parent, 'qtimetadatafield')
    fieldlabel = SubElement(field, 'fieldlabel')
    fieldlabel.text = label
    fieldentry = SubElement(field, 'fieldentry')
    fieldentry.text = value


def _create_question_item(question: Question) -> Element:
    """
    Create a QTI item element for a question.
    
    Args:
        question: The Question object to convert.
        
    Returns:
        An Element representing the QTI item.
    """
    item_id = _generate_identifier()
    
    item = Element('item')
    item.set('ident', item_id)
    item.set('title', f"Question {question.number}")
    
    # Item metadata
    itemmetadata = SubElement(item, 'itemmetadata')
    qtimetadata = SubElement(itemmetadata, 'qtimetadata')
    _add_metadata_field(qtimetadata, 'question_type', 'multiple_choice_question')
    _add_metadata_field(qtimetadata, 'points_possible', '1')
    _add_metadata_field(qtimetadata, 'original_answer_ids', 
        ','.join([f"{item_id}_{c.letter}" for c in question.choices]))
    _add_metadata_field(qtimetadata, 'assessment_question_identifierref', _generate_identifier())
    
    # Presentation
    presentation = SubElement(item, 'presentation')
    
    # Question text (material)
    material = SubElement(presentation, 'material')
    mattext = SubElement(material, 'mattext')
    mattext.set('texttype', 'text/html')
    mattext.text = _markdown_to_html(question.stem)
    
    # Response (answer choices)
    response_lid = SubElement(presentation, 'response_lid')
    response_lid.set('ident', 'response1')
    response_lid.set('rcardinality', 'Single')
    
    render_choice = SubElement(response_lid, 'render_choice')
    
    for choice in question.choices:
        choice_id = f"{item_id}_{choice.letter}"
        response_label = SubElement(render_choice, 'response_label')
        response_label.set('ident', choice_id)
        
        material = SubElement(response_label, 'material')
        mattext = SubElement(material, 'mattext')
        mattext.set('texttype', 'text/html')
        mattext.text = _markdown_to_html(choice.text)
    
    # Response processing
    resprocessing = SubElement(item, 'resprocessing')
    outcomes = SubElement(resprocessing, 'outcomes')
    decvar = SubElement(outcomes, 'decvar')
    decvar.set('maxvalue', '100')
    decvar.set('minvalue', '0')
    decvar.set('varname', 'SCORE')
    decvar.set('vartype', 'Decimal')
    
    # Correct answer condition
    if question.correct_answer:
        correct_choice_id = f"{item_id}_{question.correct_answer}"
        respcondition = SubElement(resprocessing, 'respcondition')
        respcondition.set('continue', 'No')
        
        conditionvar = SubElement(respcondition, 'conditionvar')
        varequal = SubElement(conditionvar, 'varequal')
        varequal.set('respident', 'response1')
        varequal.text = correct_choice_id
        
        setvar = SubElement(respcondition, 'setvar')
        setvar.set('action', 'Set')
        setvar.set('varname', 'SCORE')
        setvar.text = '100'
    
    return item


def create_qti_package(
    questions: List[Question],
    output_path: str,
    title: str = "Assessment"
) -> str:
    """
    Create a QTI package (ZIP file) for import into Canvas LMS.
    
    Args:
        questions: List of Question objects to convert.
        output_path: Path for the output ZIP file.
        title: Title of the assessment.
        
    Returns:
        Path to the created ZIP file.
    """
    assessment_id = _generate_identifier()
    
    # Generate XML content
    qti_xml = generate_qti_assessment(questions, title, assessment_id)
    manifest_xml = generate_qti_manifest(assessment_id, title)
    
    # Create ZIP file
    output_path = Path(output_path)
    if not output_path.suffix:
        output_path = output_path.with_suffix('.zip')
    
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        # Add manifest
        zf.writestr('imsmanifest.xml', manifest_xml)
        
        # Add assessment XML in subdirectory
        zf.writestr(f"{assessment_id}/{assessment_id}.xml", qti_xml)
    
    return str(output_path)
