<!-- 外部 JS 使用普通 script，不能添加 setup -->
<!-- <script src="./login.js"></script> -->
<script setup>
import { ref } from 'vue'

// false：隐藏密码；true：显示密码
const showPassword = ref(false)

const togglePassword = () => {
    showPassword.value = !showPassword.value
}
</script>

<template>
    <div class="login-warp">
        <!-- 左侧内容，移动端隐藏 -->
        <div class="login-left">
            <div class="left-content">
                <div class="decoration circle shape-1"></div>
                <div class="decoration circle shape-2"></div>
                <div class="decoration square shape-3"></div>
                <div class="decoration square shape-4"></div>
                <div class="decoration square shape-5"></div>
                <div class="decoration line line-1"></div>
                <div class="decoration line line-2"></div>
                <div class="dot"></div>
                <div class="left-text">
                    <h1>WELCOME BACK</h1>
                    <p>Sign in to continue your journey</p>
                </div>
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
                        <input class="username-input" type="text" placeholder="请输入账号">
                    </div>
                </div>

                <!-- 密码 -->
                <div class="form-item">
                    <div class="input-wrap">
                        <i class="bi bi-lock"></i>
                        <input class="password-input" :type="showPassword ? 'text' : 'password'" placeholder="请输入密码"
                            autocomplete="current-password" />
                        <button type="button" class="password-toggle" :aria-label="showPassword ? '隐藏密码' : '显示密码'"
                            :title="showPassword ? '隐藏密码' : '显示密码'" @click="togglePassword">
                            <i class="bi" :class="showPassword ? 'bi-eye-slash' : 'bi-eye'" aria-hidden="true"></i>
                        </button>
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
                    <!-- <button class="apple-btn-solid">
                        <i class="bi bi-box-arrow-in-right"></i>
                        登录
                    </button> -->
                    <button type="submit" class="btn-login"><span>登 录</span></button>
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
.login-warp {
    min-height: 100vh;
    display: flex;
    // background-color: var(--app-bg-page);

    // 左侧内容，移动端隐藏
    .login-left {
        width: 50%;
        background-color: var(--app-page-bg-minor);
        position: relative;
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: center;

        .left-content {

            // 几何图形
            .decoration {
                position: absolute;
                border: 1px solid rgba(0, 0, 0, 0.15);
                background: rgba(0, 0, 0, 0.02);
            }

            .circle {
                border-radius: 50%;
            }

            .square {
                border-radius: 6px;
            }

            .line {
                height: 1px;
                background: rgba(0, 0, 0, 0.2);
                border: none;
            }

            .shape-1 {
                width: 220px;
                height: 220px;
                top: 12%;
                left: 18%;
                animation: rotate 14s linear infinite;
            }

            .shape-2 {
                width: 140px;
                height: 140px;
                bottom: 18%;
                right: 22%;
                animation: rotate 18s linear infinite reverse;
            }

            .shape-3 {
                width: 80px;
                height: 80px;
                top: 55%;
                left: 55%;
                animation: floatY 7s ease-in-out infinite;
            }

            .shape-4 {
                width: 40px;
                height: 40px;
                top: 30%;
                right: 30%;
                animation: floatX 9s ease-in-out infinite;
            }

            .shape-5 {
                width: 100px;
                height: 100px;
                bottom: 30%;
                left: 30%;
                animation: rotate 22s linear infinite;
            }

            .dot {
                width: 10px;
                height: 10px;
                background: #333;
                border-radius: 50%;
                position: absolute;
                top: 40%;
                left: 40%;
                animation: pulse 3s ease-in-out infinite;
            }

            .line-1 {
                width: 260px;
                top: 48%;
                left: 50%;
                transform: translateX(-50%);
                animation: lineScale 6s ease-in-out infinite;
            }

            .line-2 {
                width: 160px;
                top: 62%;
                left: 50%;
                transform: translateX(-50%);
                animation: lineScale 7s ease-in-out infinite reverse;
            }

            @keyframes rotate {
                from {
                    transform: rotate(0deg);
                }

                to {
                    transform: rotate(360deg);
                }
            }

            @keyframes floatY {

                0%,
                100% {
                    transform: translateY(0);
                }

                50% {
                    transform: translateY(-24px);
                }
            }

            @keyframes floatX {

                0%,
                100% {
                    transform: translateX(0);
                }

                50% {
                    transform: translateX(20px);
                }
            }

            @keyframes pulse {

                0%,
                100% {
                    opacity: 0.3;
                    transform: scale(1);
                }

                50% {
                    opacity: 1;
                    transform: scale(1.4);
                }
            }

            @keyframes lineScale {

                0%,
                100% {
                    transform: translateX(-50%) scaleX(0.6);
                    opacity: 0.3;
                }

                50% {
                    transform: translateX(-50%) scaleX(1);
                    opacity: 0.8;
                }
            }

            // 标题
            .left-text {
                position: relative;
                z-index: 2;
                color: var(--app-text-title);
                text-align: center;
                padding: 0 40px;

                h1 {
                    font-size: 28px;
                    font-weight: 600;
                    letter-spacing: 2px;
                    margin-bottom: 12px;
                }

                p {
                    font-size: 14px;
                    opacity: 1;
                    letter-spacing: 1px;
                    color: var(--app-text-description);
                }
            }
        }
    }

    // 右侧内容 登录
    .login-right {
        width: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 24px;
        background-color: var(--app-page-bg-primary);

        .login-card {
            width: 100%;
            max-width: 360px;
            background-color: var(--app-card);
            border-radius: var(--app-radius-card);
            box-shadow: var(--app-card-shadow);
            padding: 40px 32px;

            // 登录标题
            .title {
                font-size: 24px;
                font-weight: 600;
                margin-bottom: 8px;
                color: var(--app-text-title);
            }

            // 提示文本
            .sub-desc {
                font-size: 14px;
                color: var(--app-text-description);
                margin-bottom: 36px;
            }

            // 登录组件
            .form-item {
                margin-bottom: 24px;
            }

            // 账号 + 密码
            .input-wrap {
                display: flex;
                align-items: center;
                padding: 0 14px;
                height: 48px;
                background-color: var(--app-input);
                border: 1px solid var(--app-border);
                border-radius: var(--app-radius-input);

                i {
                    font-size: 18px;
                    color: var(--app-text-description);
                    margin-right: 10px;
                }

                input {
                    flex: 1;
                    height: 100%;
                    border: none;
                    outline: none;
                    font-size: 15px;
                    color: var(--app-text-minor);
                    background: transparent;

                    &::placeholder {
                        color: var(--app-text-placeholder);
                    }
                }

                .password-toggle {
                    // 固定尺寸，防止按钮挤压输入框
                    flex-shrink: 0;
                    display: inline-flex;
                    align-items: center;
                    justify-content: center;

                    width: 32px;
                    height: 32px;
                    margin-left: 8px;
                    padding: 0;

                    border: none;
                    border-radius: 50%;
                    background-color: transparent;
                    color: var(--app-text-description);
                    cursor: pointer;

                    transition:
                        color 0.2s ease,
                        background-color 0.2s ease;

                    // 覆盖 .input-wrap i 原来设置的右边距
                    i {
                        margin-right: 0;
                        color: inherit;
                        font-size: 17px;
                    }
                }

                &:focus-within {
                    border-color: var(--app-input-fcous);
                }
            }

            // 登录按钮
            .btn-login {
                display: inline-block;
                border: none;
                text-align: center;
                font-size: 15px;
                padding: 14px;
                width: 100%;
                transition: all 0.5s;
                cursor: pointer;
                background-color: var(--app-btn);
                border-radius: var(--app-radius-btn);
                color: var(--app-btn-text);

                span {
                    position: relative;
                    display: inline-block;
                    transition: 0.5s;

                    &::after {
                        content: '»';
                        position: absolute;
                        /* 修复垂直居中 */
                        top: 50%;
                        transform: translateY(-50%);
                        opacity: 0;
                        right: -15px;
                        transition: 0.5s;
                    }
                }

                &:hover span {
                    padding-right: 15px;

                    &::after {
                        opacity: 1;
                        right: 0;
                    }
                }
            }

            // 记住密码 + 忘记密码
            .form-row-between {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin: 32px 0 28px;
                font-size: 14px;
                color: var(--app-text-description);

                label {
                    display: flex;
                    align-items: center;
                    gap: 8px;
                    cursor: pointer;

                    input[type="checkbox"] {
                        accent-color: var(--app-btn);
                    }
                }

                a {
                    color: var(--app-text-description);
                    text-decoration: underline;

                    &:hover {
                        color: var(--app-text-title);
                        // text-decoration: underline;
                    }
                }
            }

            // 分割线
            .divider {
                display: flex;
                align-items: center;
                margin: 28px 0;
                color: var(--app-text-description);
                font-size: 14px;

                &::before,
                &::after {
                    content: "";
                    flex: 1;
                    height: 1px;
                    background-color: var(--app-border-line);
                }

                span {
                    padding: 0 14px;
                }
            }

            // 第三方登录按钮组
            .social-login {
                display: flex;
                gap: 14px;

                .social-btn {
                    flex: 1;
                    height: 46px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    gap: 6px;
                    cursor: pointer;
                    font-size: 14px;
                    transition: background 0.5s;

                    color: var(--app-text-description);
                    background-color: var(--app-page-bg-minor);
                    border: 1px solid var(--app-border);
                    border-radius: var(--app-radius-btn);

                    &:hover {
                        background-color: var(--app-page-bg-primary);
                    }
                }
            }

            // 注册跳转提示
            .tip-text {
                margin-top: 12px;
                text-align: center;
                font-size: 14px;
                color: var(--app-text-description);

                .link-text {
                    color: var(--app-text-description);
                    text-decoration: underline;

                    &:hover {
                        color: var(--app-text-title);
                    }
                }
            }
        }
    }

    /* 手机端：隐藏左侧 */
    @media (max-width: 768px) {
        .login-left {
            display: none;
        }

        .login-right {
            width: 100%;
            height: 100vh;
            padding: 20px;
        }

        .login-card {
            padding: 32px 24px;
        }
    }
}
</style>