document.addEventListener("DOMContentLoaded", function() {
  /**
   * HomePage - Help section
   */
  class Help {
    constructor($el) {
      this.$el = $el;
      this.$buttonsContainer = $el.querySelector(".help--buttons");
      this.$slidesContainers = $el.querySelectorAll(".help--slides");
      this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
      this.init();
    }

    init() {
      this.events();
    }

    events() {
      /**
       * Slide buttons
       */
      this.$buttonsContainer.addEventListener("click", e => {
        if (e.target.classList.contains("btn")) {
          this.changeSlide(e);
        }
      });

      /**
       * Pagination buttons
       */
      this.$el.addEventListener("click", e => {
        if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
          this.changePage(e);
        }
      });
    }

    changeSlide(e) {
      e.preventDefault();
      const $btn = e.target;

      // Buttons Active class change
      [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
      $btn.classList.add("active");

      // Current slide
      this.currentSlide = $btn.parentElement.dataset.id;

      // Slides active class change
      this.$slidesContainers.forEach(el => {
        el.classList.remove("active");

        if (el.dataset.id === this.currentSlide) {
          el.classList.add("active");
        }
      });
    }

    /**
     * TODO: callback to page change event
     */
    changePage(e) {
      e.preventDefault();
      const page = e.target.dataset.page;
      switch (this.currentSlide) {
        case '1': $(".help--slides[data-id='1']").load('/?charities_page=' + page + '#help .help--slides[data-id=\'1\']'); break;
        case '2': $(".help--slides[data-id='2']").load('/?ngos_page=' + page + '#help .help--slides[data-id=\'2\']'); break;
        case '3': $(".help--slides[data-id='3']").load('/?local_collections_page=' + page + '#help .help--slides[data-id=\'3\']'); break;
      }
    }
  }
  const helpSection = document.querySelector(".help");
  if (helpSection !== null) {
    new Help(helpSection);
  }

  /**
   * Form Select
   */
  class FormSelect {
    constructor($el) {
      this.$el = $el;
      this.options = [...$el.children];
      this.init();
    }

    init() {
      this.createElements();
      this.addEvents();
      this.$el.parentElement.removeChild(this.$el);
    }

    createElements() {
      // Input for value
      this.valueInput = document.createElement("input");
      this.valueInput.type = "text";
      this.valueInput.name = this.$el.name;

      // Dropdown container
      this.dropdown = document.createElement("div");
      this.dropdown.classList.add("dropdown");

      // List container
      this.ul = document.createElement("ul");

      // All list options
      this.options.forEach((el, i) => {
        const li = document.createElement("li");
        li.dataset.value = el.value;
        li.innerText = el.innerText;

        if (i === 0) {
          // First clickable option
          this.current = document.createElement("div");
          this.current.innerText = el.innerText;
          this.dropdown.appendChild(this.current);
          this.valueInput.value = el.value;
          li.classList.add("selected");
        }

        this.ul.appendChild(li);
      });

      this.dropdown.appendChild(this.ul);
      this.dropdown.appendChild(this.valueInput);
      this.$el.parentElement.appendChild(this.dropdown);
    }

    addEvents() {
      this.dropdown.addEventListener("click", e => {
        const target = e.target;
        this.dropdown.classList.toggle("selecting");

        // Save new value only when clicked on li
        if (target.tagName === "LI") {
          this.valueInput.value = target.dataset.value;
          this.current.innerText = target.innerText;
        }
      });
    }
  }
  document.querySelectorAll(".form-group--dropdown select").forEach(el => {
    new FormSelect(el);
  });

  /**
   * Hide elements when clicked on document
   */
  document.addEventListener("click", function(e) {
    const target = e.target;
    const tagName = target.tagName;

    if (target.classList.contains("dropdown")) return false;

    if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
      return false;
    }

    if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
      return false;
    }

    document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
      el.classList.remove("selecting");
    });
  });

  /**
   * Switching between form steps
   */
  class FormSteps {
    constructor(form) {
      this.$form = form;
      this.$next = form.querySelectorAll(".next-step");
      this.$prev = form.querySelectorAll(".prev-step");
      this.$step = form.querySelector(".form--steps-counter span");
      this.currentStep = 1;

      this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
      const $stepForms = form.querySelectorAll("form > div");
      this.slides = [...this.$stepInstructions, ...$stepForms];

      this.init();
    }

    /**
     * Init all methods
     */
    init() {
      this.events();
      this.updateForm();
    }

    /**
     * All events that are happening in form
     */
    events() {
      // Next step
      this.$next.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();

          if (btn.parentElement.parentElement.dataset.step === "1") {
            this.hideInstitutions()
          }

          if (btn.parentElement.parentElement.dataset.step === "4") {
            this.displayFormInputData()
          }

          if (this.validateForm()) {
            this.currentStep++;
            this.updateForm();
          }
        });
      });

      // Previous step
      this.$prev.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep--;
          this.updateForm();
        });
      });

      // Form submit
      this.$form.querySelector("form").addEventListener("submit", e => {
        if(this.validateForm()){
          this.submit(e);
        }
      });
    }

    hideInstitutions(){
      let institutions = form.querySelectorAll("[data-step='3'] .form-group--checkbox input")
      let checked_categories = this.getCheckedCategories()

      institutions.forEach(institution => {
        institution.parentElement.parentElement.style.display = "block";
        checked_categories.forEach(category => {
          let institution_categories = institution.dataset.categories.split(" ");
          if (!institution_categories.includes(category.value)){
            institution.parentElement.parentElement.style.display = "none";
          }
        });
      });
    }

    getCheckedCategories(){
      let checked_categories = [];

      form.querySelectorAll("[data-step='1'] .form-group--checkbox input")
          .forEach(e => {
            if(e.checked) {
              checked_categories.push(e)
            }
          });

      return checked_categories
    }

    getCheckedInstitution() {
      let institutions = form.querySelectorAll("[data-step='3'] input[name='institution']")
      let institution_name = ''
      institutions.forEach(e => {if(e.checked) {institution_name = e.dataset.institutionname;}})
      return institution_name
    }

    displayFormInputData(){
      let summary_bags_categories = form.querySelector(".summary #summary-bags-categories");
      let bags_count = form.querySelector("[name=bags]").value;
      let checked_categories = this.getCheckedCategories()
      let checked_categories_names = []
      checked_categories.forEach(e => {checked_categories_names.push(e.dataset.categoryname.toLowerCase())})

      let institution_name = this.getCheckedInstitution()
      let summary_institution = form.querySelector("li #summary-institution-name")

      summary_bags_categories.innerHTML = `${bags_count} worek/worków z przedmiotami z kategorii: ${checked_categories_names.join(", ")}.`;
      summary_institution.innerHTML = `Dla organizacji "${institution_name}".`

      let summary_address = form.querySelector("li#summary-address")
      summary_address.innerHTML = form.querySelector("input[name='address']").value
      let summary_city = form.querySelector("li#summary-city")
      summary_city.innerHTML = form.querySelector("input[name='city']").value
      let summary_postcode = form.querySelector("li#summary-postcode")
      summary_postcode.innerHTML = form.querySelector("input[name='postcode']").value
      let summary_phone = form.querySelector("li#summary-phone")
      summary_phone.innerHTML = form.querySelector("input[name='phone']").value

      let summary_date = form.querySelector("li#summary-date")
      summary_date.innerHTML = form.querySelector("input[name='date']").value
      let summary_time = form.querySelector("li#summary-time")
      summary_time.innerHTML = form.querySelector("input[name='time']").value
      let summary_more_info = form.querySelector("li#summary-more_info")
      summary_more_info.innerHTML = form.querySelector("textarea[name='more_info']").value
    }

    getAddressDateInput() {
      return form.querySelectorAll(".form-section.form-section--columns input, textarea")
    }

    validateFirstStep() {
      let checked_categories = this.getCheckedCategories()
      if (checked_categories.length === 0) {
        alert('Musisz zaznaczyć przynajmniej jedną kategorię!');
        return false;
      } else {
        return true;
      }
    }

    validateSecondStep() {
      let bags_input = form.querySelector("[name=bags]").value;
      if (isNaN(bags_input) || bags_input === "") {
        alert("Musisz podać prawidłową liczbę worków!");
        return false;
      } else {
        return true;
      }
    }

    validateThirdStep() {
      let institution = this.getCheckedInstitution();
      if (institution === null || institution === "") {
        alert("Musisz wybrać organizację!")
        return false;
      } else {
        return true;
      }
    }

    validateFourthStep() {
      let inputs = this.getAddressDateInput();
      let is_complete = true;
      let is_postcode_ok = true;
      let is_phone_ok = true;
      let is_date_ok = true;
      inputs.forEach(input => {
        if( (input.value === "" || input.value === null) && input.name !== 'more_info' ) {
          is_complete = false;
        }

        if(input.value !== null) {
          if(input.name === "postcode" && !input.value.match(/^\d{2}-\d{3}/)) {
            is_postcode_ok = false;
          }

          if(input.name === "phone" && !input.value.match(/^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{3})$/)) {
            is_phone_ok = false;
          }

          if(input.name === "date") {
            let input_date = new Date(input.value);
            let today = new Date();
            if(input_date < today) {
              is_date_ok = false;
            }
          }
        }
      });

      if(!is_complete) alert("Musisz wypełnić wymagane pola!");
      if(!is_postcode_ok) alert("Musisz podać prawidłowy kod pocztowy!");
      if(!is_phone_ok) alert("Musisz podać prawidłowy numer telefonu!");
      if(!is_date_ok) alert("Musisz podać prawidłową datę!");

      return is_complete && is_postcode_ok && is_phone_ok && is_date_ok;
    }

    validateForm() {

      let result = true;

      switch (this.currentStep) {
        case 1: {
          result = this.validateFirstStep();
          break;
        }
        case 2: {
          result = this.validateSecondStep();
          break;
        }
        case 3: {
          result = this.validateThirdStep();
          break;
        }
        case 4: {
          result = this.validateFourthStep();
          break;
        }
      }

      return result
    }

    /**
     * Update form front-end
     * Show next or previous section etc.
     */
    updateForm() {
      this.$step.innerText = this.currentStep;

      this.slides.forEach(slide => {
        slide.classList.remove("active");

        if (slide.dataset.step === this.currentStep) {
          slide.classList.add("active");
        }
      });

      this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
      this.$step.parentElement.hidden = this.currentStep >= 6;

    }

    /**
     * Submit form
     *
     * TODO: validation, send data to server
     */
    submit(e) {
      e.preventDefault();
      this.currentStep++;
      this.updateForm();
      $.post("/adddonation/", $("form").serialize(), function (){
        $('section.form--steps').load('/formconfirmation# .slogan.container.container--90')
      });
    }

  }
  const form = document.querySelector(".form--steps");
  if (form !== null) {
    new FormSteps(form);
  }

  class Donations {
    constructor() {
      this.$archive_buttons = donations.querySelectorAll(".btn--archive");

      this.init();
    }

    init() {
      this.events();
    }



    events() {
      this.$archive_buttons.forEach(btn => {
        btn.addEventListener("click", e => {

          const csrftoken = getCookie('csrftoken');

          $.ajax({url: `/api/donation/${btn.value}/`,
            type: 'PATCH',
            timeout: 3000,
            data: { id: btn.value, is_taken: true },
            headers: { "X-CSRFTOKEN": csrftoken }
          })
          .fail(function(){
            alert('Error updating this model instance.');
          })
          .done(function(){
            let donation_li = btn.parentElement.parentElement
            document.querySelector('.archived-donations').appendChild(donation_li)
          });

        });
      });
    }
  }
  const donations = document.querySelector(".donations")
  if (donations !== null) {
    new Donations()
  }

  class ProfileSettings {
    constructor() {
      this.$save_button = profile_settings.querySelector("#save-button");
      this.$change_password_button = profile_settings.querySelector("#change-password-button");

      this.init();
    }

    init() {
      this.events();
    }



    events() {

      let save_btn = this.$save_button
      save_btn.addEventListener("click", e => {

        e.preventDefault()

        let csrftoken = getCookie('csrftoken');

        let email = profile_settings.querySelector("#id_username");
        let first_name = profile_settings.querySelector("#id_first_name");
        let last_name = profile_settings.querySelector("#id_last_name");
        let password = profile_settings.querySelector("#password");

        $.ajax({url: `/api/user/profile/`,
          type: 'PATCH',
          timeout: 3000,
          data: {
            username: email.value,
            first_name: first_name.value,
            last_name: last_name.value,
            password: password.value
          },
          headers: { "X-CSRFTOKEN": csrftoken }
        })
        .fail(function(){
          alert('Nie udało się zaktualizować danych. Upewnij się, że wpisane przez Ciebie hasło jest poprawne.');
        })
        .done(function(){
          alert('Twoje dane zostały pomyślnie zmienione.');
        });

      });

      let change_password_btn = this.$change_password_button
      change_password_btn.addEventListener("click", e => {

        e.preventDefault()

        let csrftoken = getCookie('csrftoken');

        let old_password = profile_settings.querySelector("#old-password");
        let new_password1 = profile_settings.querySelector("#new-password1");
        let new_password2 = profile_settings.querySelector("#new-password2");

        $.ajax({url: `/api/user/password/`,
          type: 'PATCH',
          timeout: 3000,
          data: {
            old_password: old_password.value,
            new_password1: new_password1.value,
            new_password2: new_password2.value,
          },
          headers: { "X-CSRFTOKEN": csrftoken }
        })
        .fail(function(){
          alert('Nie udało się ustawić nowego hasła. Upewnij się, że poprawnie wpisałeś wszystkie hasła.');
        })
        .done(function(){
          alert('Twoje hasło zostało pomyślnie zmienione.');
        });

      });
    }
  }
  const profile_settings = document.querySelector("#profile-settings")
  if (profile_settings !== null) {
    new ProfileSettings()
  }

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }
});
