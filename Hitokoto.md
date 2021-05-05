# 一言 相关说明
## hitokoto_type 说明
| 类型 | 说明 |
| - | - |
| a | 动画 |
| b | 漫画 |
| c | 游戏 |
| d | 文学 |
| e | 原创 |
| f | 来自网络 |
| g | 其他 |
| h | 影视 |
| i | 诗词 |
| j | 网易云 |
| k | 哲学 |
| l | 抖机灵 |


## hitokoto_text 说明
### 可用参数
`$hitokoto`: 一言内容（说的啥）  
`$from`: 一言来源（谁说的）  
`$creator`: 一言上传者（谁收集的）  

### 使用例
**源JSON**：  
```json
{
    "id": 1,
    "uuid": "9818ecda-9cbf-4f2a-9af8-8136ef39cfcd",
    "hitokoto": "与众不同的生活方式很累人呢，因为找不到借口。",
    "type": "a",
    "from": "幸运星",
    "from_who": null,
    "creator": "跳舞的果果",
    "creator_uid": 0,
    "reviewer": 0,
    "commit_from": "web",
    "created_at": "1468605909",
    "length": 22
  },
```

**hitokoto_text**：
```bash
$hitokoto —— $from \n此一言由网友\"$creator\"提供
```

**最终输出**：
```
与众不同的生活方式很累人呢，因为找不到借口。——幸运星 
此一言由网友"跳舞的果果"提供
```