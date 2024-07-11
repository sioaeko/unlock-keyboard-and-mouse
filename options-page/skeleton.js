const extension = {
    skeleton: {
        component: 'base',
        attr: {
            theme: () => satus.storage.get('theme') || 'light'
        }
    }
};

// 헤더 컴포넌트 생성 함수
function createHeaderComponent() {
    return {
        component: 'header',
        sectionStart: {
            component: 'section',
            variant: 'align-start',
            back: createBackButton(),
            title: {
                component: 'span',
                variant: 'title'
            }
        },
        sectionEnd: {
            component: 'section',
            variant: 'align-end',
            menu: createMenuButton()
        }
    };
}

// 뒤로 가기 버튼 생성 함수
function createBackButton() {
    return {
        component: 'button',
        variant: 'icon',
        attr: {
            'hidden': 'true'
        },
        on: {
            click: 'main.layers.back'
        },
        svg: {
            component: 'svg',
            attr: {
                'viewBox': '0 0 24 24',
                'stroke-width': '1.5',
                'stroke': 'currentColor',
                'fill': 'none'
            },
            path: {
                component: 'path',
                attr: {
                    'd': 'M14 18l-6-6 6-6'
                }
            }
        }
    };
}

// 메뉴 버튼 생성 함수
function createMenuButton() {
    // 메뉴 버튼의 상세 구현
}

// 스위치 컴포넌트 생성 함수
function createSwitchComponent(key, text, iconPath) {
    return {
        component: 'switch',
        before: {
            component: 'svg',
            attr: {
                'fill': 'var(--satus-primary)',
                'viewBox': '0 0 24 24'
            },
            path: {
                component: 'path',
                attr: {
                    'd': iconPath
                }
            }
        },
        text: text,
        storage: () => {
            const prefix = 'websites/' + extension.hostname;
            return satus.storage.get(prefix + '/separated') ? prefix + '/' + key : 'global/' + key;
        }
    };
}

// 메인 컴포넌트 생성
extension.skeleton.main = {
    component: 'main',
    layers: {
        component: 'layers',
        on: {
            open: function() {
                // 레이어 오픈 시 로직
            }
        },
        toolbar: {},
        section: {
            component: 'section',
            variant: 'card',
            clipboard: createClipboardButton(),
            contextmenu: createSwitchComponent('contextmenu', 'contextMenu', 'M2.38 20.57V3.07h9.5v4h9.74v13.5Z...'),
            select: createSwitchComponent('select', 'select', 'M3 5q0-.825.587-1.413Q4.175 3 5 3v2Z...'),
            drag_and_drop: createSwitchComponent('drag_and_drop', 'dragAndDrop', 'M17.8 22.8q1.88-.23 3.3-1.63 1.43-1.4 1.7-3.37...'),
            search: createSwitchComponent('search', 'search', 'm19.55 20.57-6.3-6.27q-.75.62-1.73.97...'),
            custom: createCustomButton()
        }
    }
};

// 클립보드 버튼 생성 함수
function createClipboardButton() {
    // 클립보드 버튼의 상세 구현
}

// 커스텀 버튼 생성 함수
function createCustomButton() {
    // 커스텀 버튼의 상세 구현
}

// 초기화 함수
function initializeSkeleton() {
    extension.skeleton.header = createHeaderComponent();
    // 기타 초기화 로직
}

initializeSkeleton();
