<script src="./test.js"></script>

<template>
  <main class="test-page">
    <section class="test-card">
      <h1>公共提示测试</h1>
      <p>点击按钮，检查提示的样式、位置和关闭行为。</p>

      <div class="test-buttons">
        <button type="button" @click="showSuccess">成功提示</button>
        <button type="button" @click="showError">错误提示</button>
        <button type="button" @click="showWarning">警告提示</button>
        <button type="button" @click="showInfo">普通提示</button>
        <button type="button" @click="showLongText">长文本提示</button>
        <button type="button" @click="showPersistent">不自动关闭</button>
        <button type="button" @click="closeAll">关闭全部</button>
      </div>
    </section>
  </main>
</template>

<style scoped lang="scss" src="./test.scss"></style>