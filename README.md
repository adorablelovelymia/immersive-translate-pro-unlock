# immersive-translate-pro-unlock

[沉浸式翻译 (Immersive Translate)](https://github.com/immersive-translate/immersive-translate) 的自动打包镜像，去掉了 Pro / Max 订阅的客户端校验，所有 Pro / Max 功能直接解锁。

## 工作原理

- 每天（UTC 00:00）自动监听上游最新 release，也可在 Actions 页手动 `Run workflow` 触发。
- 下载上游 3 个资产（Chrome / Firefox / Userscript），用 `patch.py` 把订阅校验函数改写为 `return true`：
  - Pro 检查：`subscription.subscriptionStatus === "active"`
  - Max 检查：`memberShip === "max" || memberType === "team"`
- 重新打包，发布为本仓库的 `v<版本号>-patched` release。

补丁基于「校验函数体」而非函数名，可兼容上游压缩器改名。若上游改动了校验代码导致 `patch.py` 匹配不到，Workflow 会**报错中止**（而非静默失效），此时需更新 `patch.py` 中的正则。

## 安装

### Chrome / Edge（Chromium 内核）

1. 从最新 release 下载 `chrome-immersive-translate-<版本>-patched.zip` 并解压。
2. 打开 `chrome://extensions`（Edge 为 `edge://extensions`）。
3. 打开右上角「开发者模式」。
4. 点「加载已解压的扩展程序」，选择解压后的目录。

### Firefox

1. 下载 `firefox-immersive-translate-<版本>-patched.xpi`。
2. 由于 `.xpi` 未签名，Firefox 稳定版不允许永久安装，需满足其一：
   - 使用 **Firefox Developer Edition / Nightly / ESR**，在 `about:config` 设 `xpinstall.signatures.required = false` 并重启，然后在 `about:addons` → 齿轮 → “从文件安装附加组件” 选择 `.xpi`。
   - 或用 `about:debugging#/runtime/this-firefox` → “临时载入附加组件” 选择 `manifest.json`（重启后失效）。
3. 也可以直接解压 `.xpi`，用上一条的临时载入方式加载其中的 `manifest.json`。

### Userscript（Tampermonkey / Violentmonkey）

1. 下载 `immersive-translate-<版本>-patched.user.js`。
2. 在脚本管理器中新建脚本，粘贴该文件内容，或直接导入安装。

## 限制

- 内置付费翻译服务（如 Transmart）仍受**服务端配额**限制，客户端解锁无法绕过；但自带 API Key 的 BYOK 服务（OpenAI / Gemini / Claude / DeepL 等）可完整使用。
- 仅修改订阅状态判断，不影响其它逻辑。

## 手动触发 / 更新补丁

- 手动触发：本仓库 Actions → `patch-release` → `Run workflow`。
- 若上游改动导致补丁失效，编辑 `patch.py` 中的 `PRO_RE` / `MAX_RE` 正则即可。

> 仅供个人学习与技术研究使用。
