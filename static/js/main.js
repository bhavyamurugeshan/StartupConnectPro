// Main JavaScript for StartupConnect
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Feather Icons
    if (typeof feather !== 'undefined') {
        feather.replace();
    }
    
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
    
    // Auto-scroll messages container to bottom
    const messagesContainer = document.getElementById('messagesContainer');
    if (messagesContainer) {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
    
    // Form validation enhancement
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            // Add loading state to submit buttons
            const submitBtns = form.querySelectorAll('input[type="submit"], button[type="submit"]');
            submitBtns.forEach(function(btn) {
                btn.disabled = true;
                const originalText = btn.textContent || btn.value;
                if (btn.tagName === 'BUTTON') {
                    btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>Loading...';
                } else {
                    btn.value = 'Loading...';
                }
                
                // Re-enable after 10 seconds (fallback)
                setTimeout(function() {
                    btn.disabled = false;
                    if (btn.tagName === 'BUTTON') {
                        btn.textContent = originalText;
                    } else {
                        btn.value = originalText;
                    }
                }, 10000);
            });
        });
    });
    
    // Smooth scrolling for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Character counter for textareas
    const textareas = document.querySelectorAll('textarea[maxlength]');
    textareas.forEach(function(textarea) {
        const maxLength = textarea.getAttribute('maxlength');
        const parent = textarea.parentNode;
        
        // Create counter element
        const counter = document.createElement('div');
        counter.className = 'form-text text-end';
        counter.innerHTML = `<span id="${textarea.id}_counter">0</span>/${maxLength}`;
        parent.appendChild(counter);
        
        const counterSpan = document.getElementById(`${textarea.id}_counter`);
        
        // Update counter on input
        textarea.addEventListener('input', function() {
            const currentLength = this.value.length;
            counterSpan.textContent = currentLength;
            
            // Change color when approaching limit
            if (currentLength > maxLength * 0.8) {
                counterSpan.className = 'text-warning';
            } else if (currentLength > maxLength * 0.9) {
                counterSpan.className = 'text-danger';
            } else {
                counterSpan.className = '';
            }
        });
        
        // Initial count
        textarea.dispatchEvent(new Event('input'));
    });
    
    // Enhanced search functionality
    const searchForm = document.querySelector('#searchForm');
    if (searchForm) {
        const searchInput = searchForm.querySelector('input[name="query"]');
        if (searchInput) {
            // Add search suggestions (could be enhanced with actual data)
            searchInput.addEventListener('focus', function() {
                // Add placeholder animation or suggestions
                this.placeholder = 'Try "AI", "FinTech", "HealthTech"...';
            });
            
            searchInput.addEventListener('blur', function() {
                this.placeholder = 'Search startups...';
            });
        }
    }
    
    // Tooltip initialization for Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Connection form toggle functionality
    window.toggleConnectionForm = function() {
        const form = document.getElementById('connectionForm');
        if (form) {
            if (form.style.display === 'none' || form.style.display === '') {
                form.style.display = 'block';
                form.scrollIntoView({ behavior: 'smooth', block: 'center' });
            } else {
                form.style.display = 'none';
            }
        }
    };
    
    // Image lazy loading for profile pictures (if implemented later)
    const images = document.querySelectorAll('img[data-src]');
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver(function(entries, observer) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        images.forEach(function(img) {
            imageObserver.observe(img);
        });
    }
    
    // Real-time message updates (could be enhanced with WebSockets)
    const messageForm = document.querySelector('form[action*="messages"]');
    if (messageForm) {
        messageForm.addEventListener('submit', function() {
            // Add animation to new messages
            setTimeout(function() {
                const messages = messagesContainer.querySelectorAll('.d-flex:last-child');
                if (messages.length > 0) {
                    messages[messages.length - 1].classList.add('message-animation');
                }
            }, 100);
        });
    }
    
    // Keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + K for search
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            const searchInput = document.querySelector('input[name="query"]');
            if (searchInput) {
                searchInput.focus();
            }
        }
        
        // Escape to close modals/forms
        if (e.key === 'Escape') {
            const connectionForm = document.getElementById('connectionForm');
            if (connectionForm && connectionForm.style.display !== 'none') {
                toggleConnectionForm();
            }
        }
    });
    
    // Progressive enhancement for better UX
    // Add loading states to navigation links
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    navLinks.forEach(function(link) {
        link.addEventListener('click', function() {
            // Add subtle loading indicator
            const icon = this.querySelector('[data-feather]');
            if (icon) {
                icon.classList.add('fa-spin');
                setTimeout(function() {
                    icon.classList.remove('fa-spin');
                }, 1000);
            }
        });
    });
    
    // Enhanced form validation messages
    const invalidFeedbacks = document.querySelectorAll('.invalid-feedback');
    invalidFeedbacks.forEach(function(feedback) {
        feedback.style.display = 'block';
        feedback.style.animation = 'fadeInUp 0.3s ease';
    });
    
    // Auto-save form data to localStorage (for longer forms)
    const longForms = document.querySelectorAll('form[data-autosave]');
    longForms.forEach(function(form) {
        const formId = form.id || 'autosave_form';
        const inputs = form.querySelectorAll('input, textarea, select');
        
        // Load saved data
        inputs.forEach(function(input) {
            const savedValue = localStorage.getItem(`${formId}_${input.name}`);
            if (savedValue && !input.value) {
                input.value = savedValue;
            }
        });
        
        // Save data on input
        inputs.forEach(function(input) {
            input.addEventListener('input', function() {
                localStorage.setItem(`${formId}_${input.name}`, input.value);
            });
        });
        
        // Clear saved data on successful submit
        form.addEventListener('submit', function() {
            setTimeout(function() {
                inputs.forEach(function(input) {
                    localStorage.removeItem(`${formId}_${input.name}`);
                });
            }, 1000);
        });
    });
});

// Utility functions
window.StartupConnect = {
    // Show notification
    showNotification: function(message, type = 'info') {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(alertDiv);
        
        // Auto dismiss
        setTimeout(function() {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    },
    
    // Format date
    formatDate: function(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
    },
    
    // Debounce function for search
    debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
};
