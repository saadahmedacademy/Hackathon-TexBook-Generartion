export const handleCitationClick = (citation: { source_url: string; section_heading: string }) => {
  const { source_url, section_heading } = citation;
  const currentPath = window.location.pathname;

  // Simple path comparison, might need to be more robust
  if (currentPath.includes(source_url)) {
    const slug = section_heading.toLowerCase().replace(/\s+/g, '-');
    const element = document.getElementById(slug);
    
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'center' });
      element.classList.add('highlighted-citation');
      setTimeout(() => {
        element.classList.remove('highlighted-citation');
      }, 3000); // Highlight for 3 seconds
    } else {
        console.warn(`Citation element with id '${slug}' not found.`);
    }
  } else {
    // If citation is on a different page, navigate to it with a hash.
    // This assumes the highlighting can be triggered on page load via the hash.
    window.location.href = `${source_url}#${section_heading.toLowerCase().replace(/\s+/g, '-')}`;
  }
};
