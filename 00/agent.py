import ollama
import json
import os

MEMORY_FILE = "agent_memory.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_to_memory(user_input, ai_response):
    memory = load_memory()
    memory.append({"user": user_input, "ai": ai_response})
    with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(memory, f, ensure_ascii=False, indent=4)

def run_agent(task, file_path=None):
    context = ""
    # استخدام المسار المطلق لضمان قراءة الملف
    if file_path and os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            context = f.read(3000) # قراءة أول 3000 حرف فقط للسرعة

    system_prompt = """أنت 'Sivar Python Architect'، خبير تطوير محترف في لغة بايثون.
مهمتك:
1. كتابة كود بايثون متوافق مع معايير PEP8.
2. التركيز على المكتبات الحديثة والأداء العالي.
3. عند التعامل مع الأخطاء، قم بتحليل الـ Traceback واقترح الحل الجذري.
4. أجب دائماً بأكواد Python احترافية وجاهزة للتنفيذ."""

    prompt = f"المهمة: {task}\n\nالسياق البرمجي:\n{context}"

    # استخدام نسخة 7b السريعة بدلاً من latest
    response = ollama.chat(
        model='qwen2.5-coder:7b', 
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': prompt},
        ],
        stream=False # إضافة لزيادة السرعة
    )
    
    ai_answer = response['message']['content']
    save_to_memory(task, ai_answer)
    return ai_answer