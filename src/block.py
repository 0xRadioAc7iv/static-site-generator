from enum import Enum
import re

markdown_heading_regex_pattern = r"^#{1,6} \w+"
markdown_code_block_regex_pattern = r"```\n[\s\S]*\n```"
markdown_quote_block_regex_pattern = r"^>[\s]?\w+"
markdown_ul_regex_pattern = r"^- \w+"
markdown_ol_regex_pattern = r"^\d+\. \w+"

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdownText: str):
    blocks = markdownText.strip().split("\n\n")
    blocks = [block for block in blocks if block != ""]
    return blocks

def block_to_block_type(block: str) -> BlockType:
    if re.match(markdown_heading_regex_pattern, block):
        return BlockType.HEADING
    if len(re.findall(markdown_code_block_regex_pattern, block)) > 0:
        return BlockType.CODE
    
    block_lines = block.split("\n")
    is_block_quote_type = True
    is_block_unordered_list_type = True

    for line in block_lines:
        if not re.match(markdown_quote_block_regex_pattern, line):
            is_block_quote_type = False
        if not re.match(markdown_ul_regex_pattern, line):
            is_block_unordered_list_type = False
        
        if not is_block_quote_type and not is_block_unordered_list_type:
            break

    if is_block_quote_type: return BlockType.QUOTE    
    if is_block_unordered_list_type: return BlockType.UNORDERED_LIST

    current_num = -1
    is_ordered_list = True
    for line in block_lines:
        if line == "":
            is_ordered_list = False
            break

        number_str = ""
        isNumMatch = re.match(r"^(\d+)\.", line)

        if isNumMatch: number_str = isNumMatch.group(1)
        if number_str and current_num == -1: current_num = int(number_str)

        if not number_str or number_str and int(number_str) != current_num:
            is_ordered_list = False
            break
        else:
            current_num += 1

    if is_ordered_list and re.match(markdown_ol_regex_pattern, block):
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH