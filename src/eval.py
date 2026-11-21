import google.generativeai as genai
from src.agent import get_chat_response

# Test cases evaluating SQL routing vs Semantic Search routing
TEST_CASES = [
    {
        "prompt": "Show me remote jobs paying over 70k", 
        "expected_concept": "Software Engineer Intern",
        "target_tool": "SQL Filtering"
    },
    {
        "prompt": "Do you have any jobs involving graph theory?", 
        "expected_concept": "Data Scientist",
        "target_tool": "Semantic Search"
    }
]

def run_evals():
    print("Starting LLM Evals...")
    score = 0
    for i, tc in enumerate(TEST_CASES):
        print(f"\nTest {i+1}: {tc['prompt']} (Target: {tc['target_tool']})")
        response = get_chat_response(f"eval_session_{i}", tc['prompt'])
        print(f"Agent Response: {response}")
        
        if tc['expected_concept'].lower() in response.lower():
            print(f"✅ PASS: Successfully retrieved {tc['expected_concept']}.")
            score += 1
        else:
            print("❌ FAIL: Expected concept missing from output.")
            
    print(f"\nFinal Eval Score: {score}/{len(TEST_CASES)}")

if __name__ == "__main__":
    run_evals()