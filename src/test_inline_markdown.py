import unittest
from inline_markdown import (
    text_to_textnodes,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    extract_markdown_images,
    extract_markdown_links,
)
from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):

    def test_delim_bold(self):
        node = TextNode("This is a text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(
            [
                TextNode("This is a text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes
        )

    def test_delim_double(self):
        node = TextNode(
            "This is a **bolded** text and another **bolded** word",
            TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" text and another ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes
        )

    def test_delim_bold_at_start(self):
        node = TextNode(
            "**Bolded** word at the start",
            TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(
            [
                TextNode("Bolded", TextType.BOLD),
                TextNode(" word at the start", TextType.TEXT),
            ],
            new_nodes
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "Now the **bolded word** has more than one word",
            TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(
            [
                TextNode("Now the ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" has more than one word", TextType.TEXT),
            ],
            new_nodes
        )

    def test_delim_italic(self):
        node = TextNode(
            "Text with an _italic_ word",
            TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)

        self.assertEqual(
            [
                TextNode("Text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes
        )

    def test_delim_bold_and_italic(self):
        node = TextNode(
            "**bold** and _italic_",
            TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)

        self.assertEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes
        )

    def test_delim_code(self):
        node = TextNode(
            "This is text with a `code block` word",
            TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes
        )

    def test_delim_with_non_text_type(self):
        node = TextNode(
            "already bolded",
            TextType.BOLD
        )
        new_nodes = split_nodes_delimiter([node], "`", TextType.BOLD)

        self.assertEqual(
            [
                TextNode("already bolded", TextType.BOLD),
            ],
            new_nodes
        )

    def test_delim_with_invalid_format(self):
        node = TextNode(
            "This is text with **invalid format",
            TextType.TEXT
        )

        self.assertRaises(
            ValueError,
            split_nodes_delimiter,
            [node], "**", TextType.BOLD
        )

    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and another link [to youtube](https://www.youtube.com)",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])

        self.assertEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and another link ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK,
                         "https://www.youtube.com"),
            ],
            new_nodes
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE,
                         "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_nodes_multipile_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])

        self.assertEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE,
                         "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE,
                         "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes
        )

    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://a.website) and ![obi wan](https://another.website)"
        extracted = extract_markdown_images(text)

        self.assertListEqual(
            [
                ("rick roll", "https://a.website"),
                ("obi wan", "https://another.website"),
            ],
            extracted
        )

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://a.website) and [to youtube](https://another.website)"
        extracted = extract_markdown_links(text)

        self.assertListEqual(
            [
                ("to boot dev", "https://a.website"),
                ("to youtube", "https://another.website"),
            ],
            extracted
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)

        self.assertEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE,
                         "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes
        )
