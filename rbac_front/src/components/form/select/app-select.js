/* ==================== Vue 相关依赖 ==================== */

import {
    computed,
    defineComponent,
    h,
} from 'vue'

/* ==================== Bootstrap 下拉箭头 ==================== */

/*
 * Element Plus 默认使用自己的 SVG 箭头。
 *
 * 网站中的普通图标统一使用 Bootstrap Icons，
 * 因此这里创建一个 Bootstrap 箭头组件，
 * 再通过 suffix-icon 传给 el-select。
 */
const SelectChevronIcon = defineComponent({
    name: 'SelectChevronIcon',

    setup() {
        return () =>
            h('i', {
                class:
                    'bi bi-chevron-down app-select__chevron',
                'aria-hidden': 'true',
            })
    },
})

/* ==================== 公共下拉框组件 ==================== */

export default defineComponent({
    name: 'AppSelect',

    /* ==================== 组件参数 ==================== */

    props: {
        /*
         * 当前选中的值。
         *
         * 支持：
         * String、Number、Boolean、Object、Array 和 null。
         */
        modelValue: {
            type: [
                String,
                Number,
                Boolean,
                Object,
                Array,
            ],
            default: null,
        },

        /*
         * 下拉选项。
         *
         * 标准格式：
         * [
         *   {
         *     label: '全部角色',
         *     value: 'all',
         *     disabled: false,
         *   },
         * ]
         */
        options: {
            type: Array,
            default: () => [],
        },

        // 没有选择内容时显示的提示
        placeholder: {
            type: String,
            default: '请选择',
        },

        /*
         * 下拉框宽度。
         *
         * 数字会自动转换成 px：
         * :width="132"
         *
         * 也可以直接传入字符串：
         * width="100%"
         * width="240px"
         */
        width: {
            type: [Number, String],
            default: '100%',
        },

        // 是否禁用
        disabled: {
            type: Boolean,
            default: false,
        },

        // 是否正在加载选项
        loading: {
            type: Boolean,
            default: false,
        },

        // 是否允许清空
        clearable: {
            type: Boolean,
            default: false,
        },

        // 是否允许搜索选项
        filterable: {
            type: Boolean,
            default: false,
        },

        // 是否允许选择多个选项
        multiple: {
            type: Boolean,
            default: false,
        },

        /*
         * 下拉面板是否匹配输入框宽度。
         *
         * 默认开启，防止手机端选项面板过宽。
         */
        fitInputWidth: {
            type: Boolean,
            default: true,
        },

        // 没有选项时显示的内容
        emptyText: {
            type: String,
            default: '暂无数据',
        },

        /*
        * 哪些值应被视为“没有选择”。
        *
        * 默认只把 undefined 当作空值。
        * 空字符串和 null 在本项目中都是有效选项：
        *
        * 空字符串：筛选未分配角色。
        * null：创建用户时暂不分配角色。
        */
        emptyValues: {
            type: Array,
            default: () => [undefined],
        },

        /*
         * 点击清空按钮后写入的值。
         *
         * 当前默认使用 undefined，
         * 避免与业务中的 null 有效选项冲突。
         */
        valueOnClear: {
            default: undefined,
        },
    },

    /* ==================== 组件事件 ==================== */

    emits: [
        'update:modelValue',
        'change',
        'clear',
        'visible-change',
        'focus',
        'blur',
    ],

    setup(props, { emit }) {
        /* ==================== 下拉框宽度 ==================== */

        const selectWidth = computed(() => {
            if (typeof props.width === 'number') {
                return `${props.width}px`
            }

            return props.width
        })

        /*
         * 通过 CSS 变量将宽度传递给样式文件。
         */
        const selectStyle = computed(() => {
            return {
                '--app-select-width':
                    selectWidth.value,
            }
        })

        /* ==================== 数据更新 ==================== */

        const handleUpdate = (value) => {
            emit('update:modelValue', value)
        }

        const handleChange = (value) => {
            emit('change', value)
        }

        const handleClear = () => {
            emit('clear')
        }

        const handleVisibleChange = (visible) => {
            emit('visible-change', visible)
        }

        const handleFocus = (event) => {
            emit('focus', event)
        }

        const handleBlur = (event) => {
            emit('blur', event)
        }

        /* ==================== 向模板暴露内容 ==================== */

        return {
            SelectChevronIcon,
            selectStyle,

            handleUpdate,
            handleChange,
            handleClear,
            handleVisibleChange,
            handleFocus,
            handleBlur,
        }
    },
})