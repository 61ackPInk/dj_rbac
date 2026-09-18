<!-- 外部 JS 使用普通 script，不能添加 setup -->
<script src="./login.js"></script>

<template>
    <div class="login-warp">
        <!-- 左侧内容，移动端隐藏 -->
        <div class="login-left">
            <div class="left contetnt">
                <h1>WELCOME BACK</h1>
                <p>Please sign in to continue.</p>
            </div>
        </div>

        <!-- 右侧内容 登录-->
        <div class="login-right">
            <div class="login-card">
                <h2 class="title">账户登录</h2>
                <div class="sub-desc">请输入你的账号信息登录系统</div>

                <!-- 账号 -->
                <div class="form-item">
                    <div class="input-wrap">
                        <i class="bi bi-person"></i>
                        <input class="username-input" type="text" placeholder="账号">
                    </div>
                </div>

                <!-- 密码 -->
                <div class="form-item">
                    <div class="input-wrap">
                        <i class="bi bi-lock"></i>
                        <input class="password-input" type="password" placeholder="密码">
                    </div>
                </div>

                <!-- 记住密码 + 忘记密码 -->
                <div class="form-row-between">
                    <label>
                        <input type="checkbox">
                        记住密码
                    </label>
                    <a href="#">忘记密码？</a>
                </div>

                <!-- 登录主按钮 -->
                <div class="form-item">
                    <button class="apple-btn-solid">
                        <i class="bi bi-box-arrow-in-right"></i>
                        登录
                    </button>
                </div>

                <!-- 分割线 -->
                <div class="divider">
                    <span>或使用以下方式登录</span>
                </div>

                <!-- 第三方登录按钮组 -->
                <div class="form-item social-login">
                    <button class="social-btn">
                        <i class="bi bi-github"></i>
                        Github
                    </button>
                    <button class="social-btn">
                        <i class="bi bi-wechat"></i>
                        微信
                    </button>
                </div>

                <!-- 注册跳转提示 -->
                <div class="tip-text">
                    还没有账号？ <a href="#" class="link-text">立即注册</a>
                </div>
            </div>
        </div>

    </div>
</template>

<!-- scoped 保证样式仅作用于当前页面 -->
<style scoped lang="scss">

</style>