import re
from enum import Enum
from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"


def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING and block.count("#", 0, 8) == 1:
            return block.lstrip("#").strip()
    raise ValueError("no title")


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    parentNodes = []
    for block in blocks:
        parentNodes.append(create_html_node_for_block(block))

    return ParentNode("div", parentNodes)


def create_html_node_for_block(block):
    block_type = block_to_block_type(block)
    match(block_type):
        case BlockType.HEADING:
            tag = f"h{block.count("#", 0, 8)}"
            block = block.lstrip("# ")
            return ParentNode(tag, text_to_children(block))
        case BlockType.CODE:
            block = block.lstrip("```\n").rstrip("```")
            code_block = text_node_to_html_node(TextNode(block, TextType.TEXT))
            code_node = ParentNode("code", [code_block])
            return ParentNode("pre", [code_node])
        case BlockType.QUOTE:
            lines = []
            for line in block.split("\n"):
                lines.append(line.lstrip(">").strip())
            block = " ".join(lines)
            return ParentNode("blockquote", text_to_children(block))
        case BlockType.ULIST:
            list_items = []
            for line in block.split("\n"):
                line = line.lstrip("- ")
                list_items.append(ParentNode("li", text_to_children(line)))
            return ParentNode("ul", list_items)
        case BlockType.OLIST:
            list_items = []
            for line in block.split("\n"):
                # TODO for now just remove the numbers. Rather use Reqex
                line = line[3:]
                list_items.append(ParentNode("li", text_to_children(line)))
            return ParentNode("ol", list_items)
        case BlockType.PARAGRAPH:
            block = " ".join(block.split("\n"))
            return ParentNode("p", text_to_children(block))
        case _:
            raise ValueError("invalid block type")


def text_to_children(text):
    children = []
    text_nodes = text_to_textnodes(text)
    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node))
    return children


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    return list(filter(None, map(str.strip, blocks)))


def block_to_block_type(block):
    if re.match(r"#{1,6} ", block):
        return BlockType.HEADING

    if block[:3] == "```" and block[-3:] == "```":
        return BlockType.CODE

    lines = block.split("\n")
    quote_lines = list(filter(lambda line: line[0] == ">", lines))
    if len(lines) == len(quote_lines):
        return BlockType.QUOTE

    ulist_lines = list(filter(lambda line: line[0:2] == "- ", lines))
    if len(lines) == len(ulist_lines):
        return BlockType.ULIST

    olist_lines = list(filter(lambda line: re.match(r"^\d\.", line), lines))
    if len(lines) == len(olist_lines):
        return BlockType.OLIST

    return BlockType.PARAGRAPH
