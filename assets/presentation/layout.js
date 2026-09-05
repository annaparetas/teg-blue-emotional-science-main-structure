/* Contain comparison tables without changing cells, IDs or generated records. */
(() => {
  document.querySelectorAll('table').forEach(table => {
    if (table.parentElement.classList.contains('presentation-table-scroll')) return;
    const columns = Math.max(...Array.from(table.rows).slice(0, 12).map(row => Array.from(row.cells).reduce((sum, cell) => sum + cell.colSpan, 0)), 1);
    table.style.setProperty('--presentation-table-width', `${Math.max(640, columns * 190)}px`);
    const region = document.createElement('div');
    region.className = 'presentation-table-scroll';
    region.tabIndex = 0;
    region.setAttribute('role', 'region');
    region.setAttribute('aria-label', table.caption?.textContent.trim() || 'Scrollable comparison table');
    table.before(region);
    region.append(table);
  });
})();
