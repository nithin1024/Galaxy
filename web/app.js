document.addEventListener("DOMContentLoaded", () => {
    loadStatsData();

    document.getElementById("btnRefresh").addEventListener("click", () => {
        const img = document.getElementById("galaxySvgImg");
        img.src = "../output/galaxy.svg?t=" + new Date().getTime();
        loadStatsData();
    });
});

async function loadStatsData() {
    try {
        const response = await fetch("../output/stats.json?t=" + new Date().getTime());
        if (!response.ok) {
            throw new Error(`Failed to load stats.json: ${response.status}`);
        }
        const data = await response.json();
        renderDashboard(data);
    } catch (err) {
        console.warn("Could not load stats.json, rendering demo state:", err);
        renderDemoFallback();
    }
}

function renderDashboard(data) {
    // User Badge
    document.getElementById("usernameText").textContent = `@${data.username}` + (data.is_mock ? " (Mock Mode)" : "");

    // Metrics
    document.getElementById("mTotalContributions").textContent = (data.total_contributions || 0).toLocaleString();
    document.getElementById("mActiveDays").textContent = `${data.active_days || 0} / ${data.total_days || 365}`;
    document.getElementById("mCurrentStreak").textContent = `${data.current_streak || 0} DAYS`;
    document.getElementById("mLongestStreak").textContent = `${data.longest_streak || 0} DAYS`;

    // Level & XP
    if (data.level) {
        document.getElementById("levelNumber").textContent = `LVL ${data.level.level}`;
        document.getElementById("levelTitle").textContent = data.level.title;
        document.getElementById("xpDetail").textContent = `${data.level.total_xp.toLocaleString()} XP`;
        document.getElementById("xpBarFill").style.width = `${data.level.progress_percent}%`;
        document.getElementById("xpProgressText").textContent = `${data.level.progress_percent}% to Level ${data.level.level + 1}`;
    }

    // Achievements
    if (data.achievements) {
        const grid = document.getElementById("achievementsGrid");
        grid.innerHTML = "";
        const unlockedCount = data.achievements.filter(a => a.unlocked).length;
        document.getElementById("unlockedCount").textContent = `${unlockedCount} / ${data.achievements.length}`;

        data.achievements.forEach(ach => {
            const item = document.createElement("div");
            item.className = `achievement-item ${ach.unlocked ? "unlocked" : ""}`;
            item.innerHTML = `
                <div class="ach-icon">${ach.icon}</div>
                <div class="ach-info">
                    <div class="ach-title">${ach.title}</div>
                    <div class="ach-desc">${ach.description}</div>
                </div>
                <div class="ach-progress">${ach.progress_text}</div>
            `;
            grid.appendChild(item);
        });
    }
}

function renderDemoFallback() {
    document.getElementById("usernameText").textContent = "@galaxy-explorer (Offline)";
    document.getElementById("mTotalContributions").textContent = "1,284";
    document.getElementById("mActiveDays").textContent = "231 / 365";
    document.getElementById("mCurrentStreak").textContent = "17 DAYS";
    document.getElementById("mLongestStreak").textContent = "42 DAYS";
    document.getElementById("levelNumber").textContent = "LVL 12";
    document.getElementById("levelTitle").textContent = "Cosmic Voyager";
    document.getElementById("xpDetail").textContent = "14,820 XP";
    document.getElementById("xpBarFill").style.width = "78%";
    document.getElementById("xpProgressText").textContent = "78% to Level 13";
}
