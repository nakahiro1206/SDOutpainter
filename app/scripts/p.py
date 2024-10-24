def generate_prompt(subject, style, quality):
    prompt = f"{subject}, {style}"
    
    if quality > 0.2:
        prompt += ", white background"
    if quality > 0.4:
        prompt += ", detailed background"
    if quality > 0.6:
        prompt += ", vibrant colors"
    if quality > 0.8:
        prompt += ", intricate textures and lighting effects"
    
    return prompt

# 使用例
print(generate_prompt("cat", "manga style", 0.1))  # 出力: "cat, manga style"
print(generate_prompt("cat", "manga style", 0.5))  # 出力: "cat, manga style, white background, detailed background"
print(generate_prompt("cat", "manga style", 0.9))  # 出力: "cat, manga style, white background, detailed background, vibrant colors, intricate textures and lighting effects"
