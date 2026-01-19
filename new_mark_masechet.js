function markMasechet(seder, masechet) {
    const chapters = MISHNA_STRUCTURE[seder][masechet].length;
    let allMarked = true;

    // Check if all are marked
    for (let c = 1; c <= chapters; c++) {
        const count = getChapterCount(masechet, c);
        const chapterId = `${masechet}-${c}`;
        for (let m = 1; m <= count; m++) {
            if (!state.progress[`${chapterId}-${m}`]) {
                allMarked = false;
                break;
            }
        }
        if (!allMarked) break;
    }

    // Toggle
    for (let c = 1; c <= chapters; c++) {
        const count = getChapterCount(masechet, c);
        const chapterId = `${masechet}-${c}`;
        for (let m = 1; m <= count; m++) {
            if (!allMarked) {
                state.progress[`${chapterId}-${m}`] = true;
            } else {
                delete state.progress[`${chapterId}-${m}`];
            }
        }
    }

    if (!allMarked) triggerConfetti();
    saveData();
    renderStudyView();
}
