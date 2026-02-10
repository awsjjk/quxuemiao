
// 全局变量存储当前登录用户
let currentUser = null;

// 登录表单处理
// const loginForm = document.getElementById('loginForm');
// const togglePassword = document.getElementById('togglePassword');
// const passwordInput = document.getElementById('password');

// 切换密码可见性
togglePassword.addEventListener('click', function() {
    const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
    passwordInput.setAttribute('type', type);

    // 切换图标
    this.querySelector('i').classList.toggle('fa-eye');
    this.querySelector('i').classList.toggle('fa-eye-slash');
});

// 处理登录表单提交
// loginForm.addEventListener('submit', function(e) {
//     e.preventDefault();
//
//     const username = document.getElementById('username').value.trim();
//     const password = passwordInput.value.trim();
//     const rememberMe = document.getElementById('rememberMe').checked;
//
//     // 简单验证
//     if (!username || !password) {
//         alert('请输入用户名和密码');
//         return;
//     }
//
//     // 模拟登录验证
//     if (password.length >= 6) {
//         // 登录成功，保存用户信息
//         currentUser = {
//             username: username,
//             // 可以添加更多用户信息
//         };
//
//         // 如果勾选了记住我，可以使用localStorage存储
//         if (rememberMe) {
//             localStorage.setItem('currentUser', JSON.stringify(currentUser));
//         } else {
//             // 否则使用sessionStorage
//             sessionStorage.setItem('currentUser', JSON.stringify(currentUser));
//         }
        // 更新页面显示
//         updateUserDisplay();
//
//         // 切换到应用界面
//         document.getElementById('loginPage').classList.add('hidden');
//         document.getElementById('app').classList.remove('hidden');
//
//         // 显示欢迎消息
//         alert(`欢迎回来，${username}！`);
//     } else {
//         alert('密码长度不能少于6位');
//     }
// });


        // 登录表单处理
    const loginForm = document.getElementById('loginForm');
    const loginPage = document.getElementById('loginPage');
    const app = document.getElementById('app');

    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const usernameInput = document.getElementById('username').value;
            const passwordInput = document.getElementById('password').value;

            // 构造请求数据
            const loginData = {
                username: usernameInput,
                password: passwordInput
            };

            // 发送 fetch 请求
            fetch('http://localhost:5000/api/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(loginData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.code === 200) {
                    // 1. 登录成功，存储 Token (可选)
                    localStorage.setItem('access_token', data.token);

                    // 2. 更新 UI 显示用户名
                    const userDisplayElements = document.querySelectorAll('.username-display');
                    userDisplayElements.forEach(el => el.textContent = data.username);

                    const userInputField = document.querySelector('.username-input');
                    if (userInputField) userInputField.value = data.username;

                    // 3. 切换界面
                    loginPage.classList.add('hidden');
                    app.classList.remove('hidden');

                    alert('登录成功！');
                } else {
                    // 4. 登录失败，显示报错信息
                    alert('登录失败: ' + (data.msg || '未知错误'));
                }
            })
            .catch(error => {
                console.error('请求出错:', error);
                alert('网络连接错误，请检查 API 是否开启');
            });
        });
    }
//

// 更新用户显示
function updateUserDisplay() {
    if (currentUser) {
        // 更新所有显示用户名的地方
        document.querySelectorAll('.username-display').forEach(element => {
            element.textContent = currentUser.username;
        });

        // 更新账号输入框
        document.querySelectorAll('.username-input').forEach(element => {
            element.value = currentUser.username;
        });
    }
}

// 检查是否有记住的登录状态
function checkLoginStatus() {
    const savedUser = localStorage.getItem('currentUser') || sessionStorage.getItem('currentUser');

    if (savedUser) {
        currentUser = JSON.parse(savedUser);
        document.getElementById('loginPage').classList.add('hidden');
        document.getElementById('app').classList.remove('hidden');
        updateUserDisplay();
    }
}

// 页面加载时检查登录状态
document.addEventListener('DOMContentLoaded', checkLoginStatus);

// 退出登录功能
document.getElementById('logoutBtn').addEventListener('click', function(e) {
    e.preventDefault();

    if (confirm('确定要退出登录吗？')) {
        // 清除用户信息
        currentUser = null;
        localStorage.removeItem('currentUser');
        sessionStorage.removeItem('currentUser');

        // 切换到登录页面
        document.getElementById('app').classList.add('hidden');
        document.getElementById('loginPage').classList.remove('hidden');

        // 重置登录表单
        loginForm.reset();
    }
});

// 导航栏滚动效果
window.addEventListener('scroll', function() {
    const navbar = document.getElementById('navbar');
    if (window.scrollY > 10) {
        navbar.classList.add('nav-scrolled');
    } else {
        navbar.classList.remove('nav-scrolled');
    }
});

// 移动端菜单切换
const mobileMenuBtn = document.getElementById('mobileMenuBtn');
const mobileMenu = document.getElementById('mobileMenu');

mobileMenuBtn.addEventListener('click', function() {
    mobileMenu.classList.toggle('hidden');
});

// 用户菜单切换
const userMenuBtn = document.getElementById('userMenuBtn');
const userMenu = document.getElementById('userMenu');

userMenuBtn.addEventListener('click', function() {
    userMenu.classList.toggle('hidden');
});

// 点击其他区域关闭用户菜单
document.addEventListener('click', function(event) {
    if (!userMenuBtn.contains(event.target) && !userMenu.contains(event.target)) {
        userMenu.classList.add('hidden');
    }
});

// 绑定孩子模态框相关
const bindChildModal = document.getElementById('bindChildModal');
const bindChildBtn1 = document.getElementById('bindChildBtn1');
const bindChildBtn2 = document.getElementById('bindChildBtn2');
const closeModalBtn = document.getElementById('closeModalBtn');
const bindChildForm = document.getElementById('bindChildForm');

// 打开模态框
function openModal() {
    bindChildModal.classList.remove('hidden');
    // 防止背景滚动
    document.body.style.overflow = 'hidden';
}

// 关闭模态框
function closeModal() {
    bindChildModal.classList.add('hidden');
    // 恢复背景滚动
    document.body.style.overflow = 'auto';
}

// 绑定打开模态框事件
bindChildBtn1.addEventListener('click', openModal);
bindChildBtn2.addEventListener('click', openModal);

// 绑定关闭模态框事件
closeModalBtn.addEventListener('click', closeModal);

// 点击模态框背景关闭
bindChildModal.addEventListener('click', function(event) {
    if (event.target === bindChildModal) {
        closeModal();
    }
});

// 绑定孩子表单提交
bindChildForm.addEventListener('submit', function(e) {
    e.preventDefault();

    const childAccount = document.getElementById('childAccount').value.trim();
    const childPassword = document.getElementById('childPassword').value.trim();

    if (childAccount && childPassword) {
        // 模拟绑定成功
        alert(`孩子账号绑定成功！\n账号：${childAccount}`);
        closeModal();
        // 清空表单
        bindChildForm.reset();
    }
});

// 个人中心按钮点击事件
function goToProfile() {
    // 隐藏所有板块
    const sections = ['home', 'school', 'reports', 'practice', 'mistakes', 'composition', 'teachers', 'tasks', 'verify'];
    sections.forEach(section => {
        const element = document.getElementById(section);
        if (element) element.classList.add('hidden');
    });

    // 显示个人中心页面
    document.getElementById('profile').classList.remove('hidden');

    // 滚动到顶部
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

document.getElementById('profileBtn').addEventListener('click', goToProfile);

// 设置按钮点击事件 - 进入个人中心页面
document.getElementById('settingsBtn').addEventListener('click', goToProfile);

// 板块切换逻辑
const sections = ['home', 'school', 'reports', 'practice', 'mistakes', 'composition', 'teachers', 'tasks', 'verify', 'profile'];

// 初始显示首页
document.getElementById('home').classList.remove('hidden');

// 为所有导航链接添加点击事件
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();

        const targetId = this.getAttribute('href').substring(1);

        // 隐藏所有板块
        sections.forEach(section => {
            const element = document.getElementById(section);
            if (element) element.classList.add('hidden');
        });

        // 显示目标板块
        const targetElement = document.getElementById(targetId);
        if (targetElement) {
            targetElement.classList.remove('hidden');

            // 滚动到顶部
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });

            // 关闭移动端菜单（如果打开）
            if (!mobileMenu.classList.contains('hidden')) {
                mobileMenu.classList.add('hidden');
            }
        }
    });
});

// 实名认证表单提交处理
document.getElementById('verificationForm')?.addEventListener('submit', function(e) {
    e.preventDefault();

    const realName = document.getElementById('realName').value.trim();
    const idCard = document.getElementById('idCard').value.trim();

    // 简单的身份证验证
    const idCardPattern = /(^\d{18}$)|(^\d{17}(\d|X|x)$)/;
    if (!idCardPattern.test(idCard)) {
        alert('请输入有效的18位身份证号码');
        return;
    }

    // 模拟认证成功
    alert(`实名认证提交成功！\n姓名：${realName}\n身份证号：${idCard.replace(/(\d{6})(\d{8})(\d{4})/, '$1********$3')}`);
});

// 筛选按钮交互 - 仅箭头图标触发
document.querySelectorAll('.filter-arrow').forEach(arrow => {
    arrow.addEventListener('click', function(e) {
        e.stopPropagation();

        // 获取当前筛选类型对应的下拉菜单
        const filterType = this.getAttribute('data-filter');
        const dropdown = this.closest('.relative').querySelector('.filter-dropdown');

        // 切换当前下拉菜单的显示状态
        dropdown.classList.toggle('open');

        // 关闭其他所有下拉菜单
        document.querySelectorAll('.filter-dropdown').forEach(otherDropdown => {
            if (otherDropdown !== dropdown) {
                otherDropdown.classList.remove('open');
            }
        });
    });
});

// 点击页面其他地方关闭所有筛选下拉菜单
document.addEventListener('click', function() {
    document.querySelectorAll('.filter-dropdown').forEach(dropdown => {
        dropdown.classList.remove('open');
    });
});

// 筛选选项点击事件
document.querySelectorAll('.filter-dropdown input').forEach(input => {
    input.addEventListener('click', function(e) {
        e.stopPropagation();

        // 显示已选筛选条件区域
        document.getElementById('selectedFilters').classList.remove('hidden');

        // 在实际应用中，这里应该根据选择的筛选条件更新老师列表
        console.log(`筛选条件变更: ${this.name}=${this.value}`);
    });
});

// 清除筛选条件
document.getElementById('clearFilters').addEventListener('click', function() {
    // 重置所有筛选选项
    document.querySelectorAll('.filter-dropdown input[type="radio"]').forEach(radio => {
        if (radio.value === 'all') {
            radio.checked = true;
        }
    });

    // 隐藏已选筛选条件区域
    document.getElementById('selectedFilters').classList.add('hidden');

    // 在实际应用中，这里应该重置老师列表显示全部
    console.log('清除所有筛选条件');
});

// 移除单个筛选条件
document.querySelectorAll('#selectedFilters button').forEach(btn => {
    btn.addEventListener('click', function(e) {
        e.stopPropagation();

        // 移除当前筛选标签
        const filterTag = this.parentElement;
        filterTag.remove();

        // 如果没有筛选标签了，隐藏整个区域
        if (document.querySelectorAll('#selectedFilters span').length === 0) {
            document.getElementById('selectedFilters').classList.add('hidden');
        }

        // 在实际应用中，这里应该根据剩余筛选条件更新老师列表
        console.log('移除筛选条件');
    });
});

// 任务中心标签页切换
const myTasksTab = document.getElementById('myTasksTab');
const publishTaskTab = document.getElementById('publishTaskTab');
const myTasksContent = document.getElementById('myTasksContent');
const publishTaskContent = document.getElementById('publishTaskContent');

myTasksTab.addEventListener('click', function() {
    // 切换标签样式
    myTasksTab.classList.add('text-primary', 'border-b-2', 'border-primary');
    myTasksTab.classList.remove('text-gray-500');
    publishTaskTab.classList.remove('text-primary', 'border-b-2', 'border-primary');
    publishTaskTab.classList.add('text-gray-500');

    // 切换内容
    myTasksContent.classList.remove('hidden');
    publishTaskContent.classList.add('hidden');

    // 检查任务列表是否为空
    checkTasksEmpty();
});

publishTaskTab.addEventListener('click', function() {
    // 切换标签样式
    publishTaskTab.classList.add('text-primary', 'border-b-2', 'border-primary');
    publishTaskTab.classList.remove('text-gray-500');
    myTasksTab.classList.remove('text-primary', 'border-b-2', 'border-primary');
    myTasksTab.classList.add('text-gray-500');

    // 切换内容
    publishTaskContent.classList.remove('hidden');
    myTasksContent.classList.add('hidden');

    // 重置表单
    document.getElementById('publishTaskForm').reset();
});

// 空状态检查
function checkTasksEmpty() {
    const taskItems = document.querySelectorAll('#myTasksContent .border.border-gray-100');
    const noTasks = document.getElementById('noTasks');

    if (taskItems.length === 0) {
        noTasks.classList.remove('hidden');
    } else {
        noTasks.classList.add('hidden');
    }
}

// 从空状态发布任务
document.getElementById('emptyStatePublishBtn').addEventListener('click', function() {
    publishTaskTab.click();
});

// 取消发布任务
document.getElementById('cancelPublishBtn').addEventListener('click', function() {
    myTasksTab.click();
});

// 发布任务表单提交
document.getElementById('publishTaskForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const subject = document.getElementById('taskSubject').value;
    const goal = document.getElementById('taskGoal').value;
    const grade = document.getElementById('taskGrade').value;
    const time = document.getElementById('taskTime').value;
    const salary = document.getElementById('taskSalary').value;
    const address = document.getElementById('taskAddress').value;

    // 简单验证
    if (!subject || !goal || !grade || !time || !salary || !address) {
        alert('请填写所有必填字段');
        return;
    }

    // 格式化时间显示
    const date = new Date(time);
    const formattedDate = date.toLocaleDateString('zh-CN');

    // 获取学科名称
    const subjectSelect = document.getElementById('taskSubject');
    const subjectName = subjectSelect.options[subjectSelect.selectedIndex].text;

    // 获取年级名称
    const gradeSelect = document.getElementById('taskGrade');
    const gradeName = gradeSelect.options[gradeSelect.selectedIndex].text;

    // 生成新任务ID
    const newTaskId = Date.now().toString();

    // 创建新任务元素并添加到列表
    const taskList = document.getElementById('myTasksContent');
    const newTask = document.createElement('div');
    newTask.className = 'border border-gray-100 rounded-lg overflow-hidden hover:shadow-md transition-shadow';
    newTask.innerHTML = `
        <div class="p-4">
            <div class="flex justify-between items-start">
                <div>
                    <h3 class="font-semibold text-gray-800">${gradeName}${subjectName}家教</h3>
                    <p class="text-sm text-gray-500 mt-0.5">${subjectName} | ${gradeName} | ${formattedDate}</p>
                </div>
                <div class="flex items-center bg-light text-primary px-2 py-1 rounded text-sm">
                    <i class="fa fa-money mr-1"></i> ${salary}元/小时
                </div>
            </div>
            <p class="text-sm text-gray-600 mt-2 line-clamp-2">
                ${goal}
            </p>
            <div class="flex flex-wrap gap-2 mt-3 text-sm">
                <span class="text-gray-500"><i class="fa fa-map-marker mr-1"></i> ${address}</span>
                <span class="text-gray-500"><i class="fa fa-clock-o mr-1"></i> ${date.toLocaleTimeString('zh-CN')}</span>
            </div>
            <div class="flex justify-end gap-3 mt-4">
                <button class="edit-task-btn border border-primary text-primary hover:bg-primary/10 font-medium py-1 px-4 rounded transition-colors" data-id="${newTaskId}">
                    <i class="fa fa-edit mr-1"></i> 修改
                </button>
                <button class="delete-task-btn bg-gray-100 text-gray-700 hover:bg-gray-200 font-medium py-1 px-4 rounded transition-colors" data-id="${newTaskId}">
                    <i class="fa fa-trash mr-1"></i> 删除
                </button>
            </div>
        </div>
    `;

    // 添加到任务列表顶部
    taskList.insertBefore(newTask, taskList.firstChild);

    // 为新添加的按钮绑定事件
    newTask.querySelector('.edit-task-btn').addEventListener('click', function() {
        // 编辑功能需要额外实现
        alert('编辑功能需要额外实现');
    });

    newTask.querySelector('.delete-task-btn').addEventListener('click', function() {
        if (confirm('确定要删除这个任务吗？')) {
            newTask.remove();
            checkTasksEmpty();
        }
    });

    // 切换到我的任务标签页
    myTasksTab.click();
    alert('任务发布成功！');
});

// 编辑任务按钮点击
document.querySelectorAll('.edit-task-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        alert('编辑功能需要额外实现');
    });
});

// 删除任务按钮点击
document.querySelectorAll('.delete-task-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        if (confirm('确定要删除这个任务吗？')) {
            this.closest('.border.border-gray-100').remove();
            checkTasksEmpty();
        }
    });
});
