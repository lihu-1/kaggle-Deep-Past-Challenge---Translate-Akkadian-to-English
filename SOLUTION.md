# Deep Past 阿卡德语翻译推理方案

## 任务

将阿卡德语转写文本翻译为英语，生成 Kaggle `submission.csv`。仓库保留两条推理路线，需分别运行并比较，不能视为已合并的单一方案。

## 方案一：ByT5 单模型

入口：[dpc-starter-infer-3-16new.ipynb](dpc-starter-infer-3-16new.ipynb)。

使用 ByT5 tokenizer 和微调的 seq2seq 模型；输入转写经过规范化后分批生成，配置 batch size 16、4 beams、最多生成 512 tokens。对译文进行后处理并写入提交文件，同时检查空预测。模型来自 Kaggle 数据集 `lihu6666/36-5modelbyt5`。

## 方案二：多模型候选与 MBR

入口：[akkadian-ensemble-0164a8.ipynb](akkadian-ensemble-0164a8.ipynb)。

对转写做预处理，按长度分桶以减少 padding；配置三个 ByT5 检查点，分别生成候选译文并汇合，再通过最小贝叶斯风险（MBR）选择最终结果。配置中包含 8 beams、每次 4 个 beam 候选、自适应 beam 和定期检查点。输出提交文件、日志及配置记录。

## 运行与比较

在 Kaggle 挂载比赛数据及相应 notebook 中的模型路径；集成方案还需要指定的离线 NLP wheel。按照单元格顺序运行，检查提交 ID 和译文。单模型更简洁；集成方案需要更多模型资源，实际耗时和效果应在相同验证集上测量。仓库不含模型权重，本次未重新运行或验证成绩。
