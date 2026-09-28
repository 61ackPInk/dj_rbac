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

/* ==================== null 选项内部占位值 ==================== */

/*
 * Element Plus 的 ElOption 不允许 value 为 null。
 *
 * 但 RBAC 项目中的 null 有明确业务含义：
 * 例如“暂不分配角色”。
 *
 * 因此在 AppSelect 内部使用一个唯一对象代替 null，
 * 对外仍然保持 null，不影响接口提交。
 */
const NULL_OPTION_VALUE = Object.freeze({
    __appSelectNullValue: true,
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
        /* ==================== 选项数据转换 ==================== */

        /*
         * 将 value 为 null 的选项转换为内部占位对象，
         * 避免 ElOption 出现类型警告。
         */
        const normalizedOptions = computed(() => {
            return props.options.map(
                (option, index) => {
                    return {
                        ...option,

                        /*
                         * 模板循环使用的稳定标识。
                         */
                        appSelectKey:
                            `${index}-${String(option.value)}`,

                        /*
                         * Element Plus 实际接收的值。
                         */
                        appSelectValue:
                            option.value === null
                                ? NULL_OPTION_VALUE
                                : option.value,
                    }
                },
            )
        })

        /*
         * 判断当前选项中是否存在 null 业务值。
         */
        const hasNullOption = computed(() => {
            return props.options.some((option) => {
                return option.value === null
            })
        })

        /*
         * 如果当前业务值是 null，
         * 并且选项中确实存在 null 选项，
         * 则向 Element Plus 传入内部占位对象。
         */
        const selectModelValue = computed(() => {
            if (
                props.modelValue === null &&
                hasNullOption.value
            ) {
                return NULL_OPTION_VALUE
            }

            return props.modelValue
        })

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
            /*
             * 用户选择内部 null 占位选项时，
             * 对外重新发送真正的 null。
             */
            const businessValue =
                value === NULL_OPTION_VALUE
                    ? null
                    : value

            emit(
                'update:modelValue',
                businessValue,
            )
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

            normalizedOptions,
            selectModelValue,
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