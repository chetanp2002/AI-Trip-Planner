from crewai.tools import BaseTool
from duckduckgo_search import DDGS
import requests
from bs4 import BeautifulSoup
import ast
import operator
import re

class SearchTool(BaseTool):
    name: str = "Search the internet"
    description: str = "Useful to search the internet about a given topic and return relevant results"

    def _run(self, query: str) -> str:
        try:
            ddgs = DDGS()
            # --- AGGRESSIVE FIX 1: Max results = 1 ---
            results = ddgs.text(keywords=query, max_results=1)
            
            if not results:
                return "No results found."
                
            formatted_results = []
            for result in results:
                # --- AGGRESSIVE FIX 2: Limit snippet to 200 chars ---
                body = result.get('body', 'N/A')[:200]
                formatted_results.append(
                    f"Title: {result.get('title', 'N/A')}\n"
                    f"Snippet: {body}...\n"
                    "-----------------"
                )
            return "\n".join(formatted_results)
            
        except Exception as e:
            return f"Error performing search: {str(e)}"

class ScrapeTool(BaseTool):
    name: str = "Scrape website content"
    description: str = "Useful to scrape and summarize a website content"

    def _run(self, website: str) -> str:
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            response = requests.get(website, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            text = soup.get_text(separator=' ', strip=True)
            
            # --- AGGRESSIVE FIX 3: Limit scrape to 500 chars ---
            return text[:500] 
            
        except Exception as e:
            return f"Error scraping site: {e}"

class CalculatorTool(BaseTool):
    name: str = "Make a calculation"
    description: str = "Useful to perform any mathematical calculations like sum, minus, multiplication, division, etc."

    def _run(self, operation: str) -> str:
        try:
            allowed_operators = {
                ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
                ast.Div: operator.truediv, ast.Pow: operator.pow, ast.Mod: operator.mod,
                ast.USub: operator.neg, ast.UAdd: operator.pos,
            }
            clean_op = re.sub(r'[^0-9+\-*/().% ]', '', operation)
            tree = ast.parse(clean_op, mode='eval')
            
            def _eval_node(node):
                if isinstance(node, ast.Expression): return _eval_node(node.body)
                elif isinstance(node, ast.Constant): return node.value
                elif isinstance(node, ast.BinOp):
                    return allowed_operators[type(node.op)](_eval_node(node.left), _eval_node(node.right))
                elif isinstance(node, ast.UnaryOp):
                    return allowed_operators[type(node.op)](_eval_node(node.operand))
                raise ValueError(f"Unsupported node type: {type(node).__name__}")
            
            return str(_eval_node(tree))
        except Exception as e:
            return f"Error: {str(e)}"