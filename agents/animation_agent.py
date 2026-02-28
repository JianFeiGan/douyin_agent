"""
动画优化 Agent
负责将文本内容转化为适合动画视频的描述
"""
from .base import BaseAgent
from typing import Dict, Any, List


class AnimationAgent(BaseAgent):
    """动画创作专家"""
    
    def __init__(self, config: Dict = None):
        super().__init__("AnimationAgent", config)
    
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        将内容转化为动画描述
        
        Args:
            input_data: {
                "content": "原始文本内容",
                "keywords": ["关键词列表"],
                "style": "内容风格",
                "task_id": "任务ID"
            }
            
        Returns:
            {
                "scenes": [
                    {"description": "场景描述", "action": "动作描述"},
                    ...
                ],
                "visual_style": {
                    "color": "色调",
                    "elements": "视觉元素",
                    "effects": "特效"
                },
                "seedance_prompt": "用于 Seedance 的英文描述"
            }
        """
        content = input_data.get("content", "")
        keywords = input_data.get("keywords", [])
        style = input_data.get("style", "通用")
        task_id = input_data.get("task_id", "unknown")
        
        self.log(f"开始动画优化 - 风格: {style}")
        
        # 1. 设计场景
        scenes = self._design_scenes(content, keywords, style)
        
        # 2. 编排动作
        actions = self._orchestrate_actions(scenes)
        
        # 3. 定义视觉风格
        visual_style = self._define_visual_style(style, keywords)
        
        # 4. 生成 Seedance prompt
        seedance_prompt = self._generate_seedance_prompt(scenes, visual_style)
        
        result = {
            "scenes": scenes,
            "actions": actions,
            "visual_style": visual_style,
            "seedance_prompt": seedance_prompt
        }
        
        self.log(f"动画优化完成 - 场景数: {len(scenes)}")
        
        # 保存结果
        self.save_result(result, task_id)
        
        return result
    
    def _design_scenes(self, content: str, keywords: List[str], style: str) -> List[Dict[str, str]]:
        """设计场景"""
        scenes = []
        
        # 根据内容长度决定场景数
        if len(content) < 100:
            num_scenes = 2
        elif len(content) < 200:
            num_scenes = 3
        else:
            num_scenes = 4
        
        # 场景模板
        scene_templates = {
            "科技感": [
                "futuristic tech laboratory with holographic displays",
                "neural network visualization with glowing nodes",
                "data streams flowing through digital circuits",
                "advanced computer systems and AI processors"
            ],
            "美食": [
                "modern kitchen with fresh ingredients",
                "cooking process with steam rising",
                "delicious food presentation",
                "warm dining atmosphere"
            ],
            "风景": [
                "breathtaking natural landscape",
                "beautiful scenery at golden hour",
                "serene nature with mountains and water",
                "stunning sunset over scenic views"
            ],
            "搞笑": [
                "playful cartoon characters",
                "funny animation with bouncy movements",
                "comedic situation with exaggerated expressions",
                "humorous scenario with surprise elements"
            ],
            "教育": [
                "clean classroom environment",
                "teacher explaining concepts with visual aids",
                "students engaged in learning activities",
                "educational graphics and diagrams"
            ],
            "通用": [
                "clean modern background",
                "dynamic scene with relevant imagery",
                "engaging visual composition",
                "professional looking environment"
            ]
        }
        
        templates = scene_templates.get(style, scene_templates["通用"])
        
        for i in range(num_scenes):
            scenes.append({
                "description": templates[i] if i < len(templates) else templates[-1],
                "action": f"scene {i+1} with smooth animation"
            })
        
        return scenes
    
    def _orchestrate_actions(self, scenes: List[Dict[str, str]]) -> List[str]:
        """编排动作"""
        actions = []
        for i, scene in enumerate(scenes):
            actions.append(f"camera slowly pans across scene {i+1}, smooth motion")
        
        return actions
    
    def _define_visual_style(self, style: str, keywords: List[str]) -> Dict[str, str]:
        """定义视觉风格"""
        style_config = {
            "科技感": {
                "color": "blue and cyan tones with neon highlights",
                "elements": "holographic displays, neural networks, futuristic equipment, glowing particles",
                "effects": "glow effects, digital transitions, particle systems"
            },
            "美食": {
                "color": "warm orange and yellow tones",
                "elements": "steam, fresh ingredients, warm lighting, delicious food",
                "effects": "steam rising, warm glow, smooth camera movements"
            },
            "风景": {
                "color": "natural greens and blues with golden hour warmth",
                "elements": "mountains, water, trees, clouds, natural light",
                "effects": "soft focus, natural transitions, ambient lighting"
            },
            "搞笑": {
                "color": "bright and vibrant colors",
                "elements": "cartoon characters, expressive elements, bouncy objects",
                "effects": "bounce animations, squash and stretch, comic effects"
            },
            "教育": {
                "color": "clean white and blue tones",
                "elements": "charts, diagrams, clean lines, organized elements",
                "effects": "smooth transitions, highlight effects, clean animations"
            },
            "通用": {
                "color": "balanced and professional colors",
                "elements": "relevant imagery, clean composition, modern design",
                "effects": "smooth transitions, professional polish"
            }
        }
        
        return style_config.get(style, style_config["通用"])
    
    def _generate_seedance_prompt(self, scenes: List[Dict], visual_style: Dict) -> str:
        """生成 Seedance 提示词"""
        # 组合场景描述
        scene_text = ", ".join([s["description"] for s in scenes])
        
        # 添加视觉风格
        prompt = f"{scene_text}, {visual_style['color']}, {visual_style['elements']}, {visual_style['effects']}, smooth animations, 9:16 vertical video"
        
        # 限制长度
        if len(prompt) > 200:
            prompt = prompt[:197] + "..."
        
        return prompt
