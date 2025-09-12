# repositories/services/map_ai_service.py

import os
import json
from openai import OpenAI
from repositories.services.map_service import build_file_imports

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_map_with_ai(repo_id: int):
    
    repo_json = build_file_imports(repo_id)

    
    prompt = f"""
        You are given the following repository structure with files and their imports:

        {json.dumps(repo_json, indent=2)}

        Your task is to produce a JSON object describing the dependency graph.

        Rules:
        1. Output only **raw JSON** (no markdown, no explanations).
        2. JSON must have this format:
        {{
            "nodes": [{{"id": "file_path", "label": "file_name"}}],
            "edges": [{{"source": "file_path", "target": "file_path"}}]
        }}

        3. Create one node for each file in the repo (use "id" = path, "label" = file).
        4. Create edges based on:
        - **Imports**: If file A imports/uses file B, add `{{"source": "A", "target": "B"}}`.
        - **Inheritance**: If `class X extends Y`, add edge from X → Y.
        - **Traits**: If `class X uses SomeTrait`, add edge from X → Trait file (if present).
        5. Ignore any import that does not match a file in the repo (e.g., "Illuminate...", "Symfony...", "JWT...", "React...", "Django...", "Flask...", etc.).
        6. Do not invent nodes. Only reference files that exist in the given repo list.
        7. Use "source" and "target" (not "from"/"to").
        8. JSON must be syntactically valid — no comments, no extra text, no markdown fences.

        Return only the JSON.
        """

    
    response = client.chat.completions.create(
        model="gpt-4o-mini",  
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    result_text = response.choices[0].message.content.strip()

    try:
        return json.loads(result_text)  
    except Exception:
        
        return {"error": "Invalid JSON from AI", "raw": result_text}
