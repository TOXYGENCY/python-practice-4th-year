from typing import List

board = [["o","a","a","n"],["e","t","a","e"],["i","h","k","r"],["i","f","l","v"]] 
words = ["oath","pea","eat","rain"]
# Output: ["eat","oath"]

class Solution:
    # Returns the all nearby letters. Recieves current letter coordinates in indexes.
    def letters_nearby(board: List[List[str]], idx1: int, idx2: int) -> List[str]:
        possible_letters = []

        # Left letter
        if (idx2 != 0):
            possible_letters.append(board[idx1][idx2-1])
        else:
            possible_letters.append("")

        # Upper letter
        if (idx1 != 0):
            possible_letters.append(board[idx1-1][idx2])
        else:
            possible_letters.append("")

        # Right letter
        if (idx2 != m-1):
            possible_letters.append(board[idx1][idx2+1])
        else:
            possible_letters.append("")

        # Bottom letter
        if (idx2 != n-1):
            possible_letters.append(board[idx1+1][idx2])
        else:
            possible_letters.append("")

        return possible_letters

    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:
        for word in words:
            letters = list(word)
            
        return [""]

Solution.findWords(Solution, board, words)