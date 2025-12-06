const getScope = () => window.angular.element('[view="offer"]').scope() || window.angular.element('body').scope();

const errorFields = {
  payment: [{
    id: 'custom-price-amount-input-wrapper',
    regex: /Amount should be/i
  }, {
    selector: '.new-card-form .table-form-inline .field-card-number .field-wrapper',
    regex: /credit card|declined|expired/i
  }, {
    selector: '.new-card-form .table-form-inline .field-card-cvv .field-wrapper',
    regex: /cvv/i
  }, {
    selector: '.new-card-form .table-form-inline .field-card-postal-code .field-wrapper',
    regex: /zip|postal|not seem to be valid/i
  }, {
    selector: '.new-card-form .table-form-inline .field-card-expiry-month .field-wrapper',
    regex: /date/i
  }],
  gift: [{
    id: 'recipientEmail',
    regex: /email/i
  }]
};

/**
 * Clear out the validation errors
 */
const removeValidationErrors = () => {
  const scope = getScope();
  const formType = scope.selectedTerm.type;
  errorFields[formType].forEach(fieldInfo => {
    var _targetField$nextElem;
    const targetField = fieldInfo.id ? document.getElementById(fieldInfo.id) : document.querySelector(fieldInfo.selector);
    targetField === null || targetField === void 0 ? void 0 : targetField.classList.remove('checkout__error', 'checkout__input--invalid', 'field-wrapper--error');
    if (targetField !== null && targetField !== void 0 && (_targetField$nextElem = targetField.nextElementSibling) !== null && _targetField$nextElem !== void 0 && _targetField$nextElem.classList.contains('checkout__error')) {
      targetField.nextElementSibling.remove();
    }
  });
};
let hadErrors = false;

/**
 *  Handle checkout errors by watching the scope.error property.  This populates when the error bar contains message strings
 */
const handleCheckoutErrors = () => {
  let scope = getScope();
  scope.$watch('hasErrors()', () => {
    var _scope, _scope$errors, _scope2, _scope2$errors;
    scope = getScope();
    // if there are no errors in the scope.errors watcher and there had previously been an error in the checkout, clear out the errors
    if (!((_scope = scope) !== null && _scope !== void 0 && (_scope$errors = _scope.errors) !== null && _scope$errors !== void 0 && _scope$errors.length) && hadErrors) {
      removeValidationErrors();
    }
    if ((_scope2 = scope) !== null && _scope2 !== void 0 && (_scope2$errors = _scope2.errors) !== null && _scope2$errors !== void 0 && _scope2$errors.length) {
      hadErrors = true;
      scope.errors.forEach(scopeError => {
        const formType = scope.selectedTerm.type;
        const errorClass = formType !== 'payment' && 'checkout__input--invalid';

        // parse out the error and match it to the css selector to put it under the input
        errorFields[formType].forEach(fieldInfo => {
          const targetField = fieldInfo.id ? document.getElementById(fieldInfo.id) : document.querySelector(fieldInfo.selector);
          if (targetField && targetField && scopeError.message.match(fieldInfo.regex)) {
            var _targetField$nextElem2;
            targetField.classList.add(errorClass, 'checkout_error', 'field-wrapper--error');

            // dont add a new error if it already has one
            if (!((_targetField$nextElem2 = targetField.nextElementSibling) !== null && _targetField$nextElem2 !== void 0 && _targetField$nextElem2.classList.contains('checkout__error'))) {
              const tempDiv = document.createElement("div");
              tempDiv.classList.add('checkout__error');
              tempDiv.textContent = scopeError.message;
              targetField.insertAdjacentElement("afterend", tempDiv);
            }
          }
        });
        /**
          *  Add error only to field that needs to be changed
          *  From piano support email:
          *    If the CVV or expiration date entered is invalid, the error message "Credit card has been declined" will show.
          *    If the credit card number is invalid, the error "Invalid credit card number" will show.
          *    If the zip code entered is invalid, the error "The card information you provided does not seem to be valid" should appear.
         **/
      });
    }
  });
};

const messageParent = message => {
  const affiliate = getScope().custom && getScope().custom.origin;
  affiliate && top.postMessage(message, affiliate);
};

const init = () => {
  const scope = getScope();
  handleCheckoutErrors();
  scope.$apply();
};
let built = false;

/**
 * moves the content fields into a config property on the scope for the custom-event
 * @param {Object} options - content fields
 */
const commonBuildSteps = options => {
  const scope = getScope();
  Object.assign(scope, options);
  scope.config = options;
  scope.$apply();
  scope.affiliate = scope.custom.origin;
};

/*
 * merge options and message main window
 * {Object} options - options to merge into scope
 */
const build = (options = {}) => {
  commonBuildSteps(options);
};

/*
* called from the checkout template to set selectedTerm and merge variables
* {Object} options - params to merge
*/
const buildSystem = (options = {}) => {
  commonBuildSteps(options);
};

/*
 * pass in an init method to load when piano loads
 * {Function} initMethod - method to init with after load
 */
const start = initMethod => {
  getScope().$on('loaded', () => {
    !built && initMethod();
    built = true;
  });
  try {
    !built && initMethod(); // if the load event has run before piano processed our script directive
    built = true;
  } catch (e) {
    built = false;
  }
};
window.Advance = {
  piano: {
    start,
    build,
    buildSystem,
    messageParent
  }
};
init();
//# sourceMappingURL=piano-frame.js.map
