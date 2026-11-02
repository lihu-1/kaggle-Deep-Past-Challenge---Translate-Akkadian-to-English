# Deep Past 阿卡德语翻译推理方案

> **当前状态：**本文介绍目前的最终推理方案；其余内容仍在制作与复盘中，后续将逐步补充。

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

## 共同的输入规范化

两个 notebook 均针对转写文本做批量规范化：空值转为空字符串，处理 `sz → š`、`s, → ṣ`、`t, → ṭ` 及带数字的元音标记；统一文本缺损标记，处理限定符、部分字符和分数表示，最后整理空白。单模型版本还显式使用 Unicode NFC。具体正则规则较多，训练与推理应使用相同版本的预处理，不宜仅凭此摘要替代代码。

## 单模型：推理链路

1. 从 `test.csv` 读取转写，添加任务前缀 `translate Akkadian to English: `。
2. 使用指定 ByT5 tokenizer 和 seq2seq checkpoint，输入最长 512 tokens，batch size 16；根据 CUDA 可用性选择 GPU 或 CPU。
3. 采用 4-beam 解码，最多生成 512 tokens，解码后对空白、控制字符、缺损标记、重复片段和分数等做较保守的后处理。
4. 空译文使用固定备用句，输出 `id, translation` 到 `submission.csv`，打印译文长度与空预测统计。

## 集成方案：候选生成与选择

### 模型和批处理

配置三个独立 checkpoint：`assiaben/final-byt5`、`mattiaangeli/byt5-akkadian-mbr-v2` 及 `lihu6666/3k-800databyt5`。模型依次加载和卸载，减少同时驻留显存的压力。输入上限 512、生成上限 384、batch size 2；按词数排序分为 6 个长度桶以减少 padding，并支持混合精度和 BetterTransformer。

### 候选池

每个模型为每条文本生成 4 个 beam 候选及 2 个采样候选。默认 8 beams、length penalty 1.3、repetition penalty 1.2；短批次的 token 长度中位数小于 100 时，自适应缩为 4 beams。采样使用 top-p 0.92、temperature 0.75。三个模型的候选按样本 ID 汇合后统一后处理和去重；候选池上限 32。

### MBR 选择

对候选两两计算 chrF++，选择与其他候选平均一致性最高的译文。该过程寻找候选之间的共识，并不直接访问真实参考译文，也不保证选中最准确的译文。后处理涵盖缺损、重复、标点、部分词汇及格式清理；候选为空时使用固定备用句。每 200 条写检查点，并输出日志、配置和提交 CSV。

## 对比与复现

单模型只加载一个 checkpoint，流程较简洁；集成方案以额外生成和两两比较换取候选共识，通常需要更多时间与计算资源，实际效果需在相同验证集上评估。两条路线的输出长度上限、batch size 和后处理力度不同，不能将差异简单归因于模型数量。本仓库没有训练代码、权重和比赛数据，也没有本次独立评测结果。
