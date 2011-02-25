(function($) {
$.extend(
		$.fn, {
			valForm : function (type) {
			
				if (!$(this).length) {return;}
				
				$(this).each (function() {
					var val = new $.val(this, type);			
					val.init();								
				}); 
			}
		}
);

$.val = function (form, type) {
	
	this.form = form;
	this.email = $(this.form).find($.val.valElements.email);
	this.integer = $(this.form).find($.val.valElements.integer);
	this.toggle = $(this.form).find($.val.valElements.toggle);
	this.login = $(this.form).find($.val.valElements.login);
	this.password = $(this.form).find($.val.valElements.password);
	this.showError = this.showValid = this.showDefault = function(){};
	
	if (type = 'fast-login') {
		
		this.showError = function(element){
			
			$(element).removeClass('fast-login-def');
			$(element).removeClass('fast-login-val');
			$(element).addClass('fast-login-err');
		}
		
		this.showValid = function(element){
			
			$(element).removeClass('fast-login-def');
			$(element).removeClass('fast-login-err');
			$(element).addClass('fast-login-val');
		}
		
		this.showDefault = function(element){
			
			$(element).removeClass('fast-login-val');
			$(element).removeClass('fast-login-err');
			$(element).addClass('fast-login-def');
		}		
	}	
}

$.extend($.val, {			
			msg: {
				required: "This field is required.",
				digits: "Please enter only digits.",
				email: "Please enter a valid email address."				
			},			
			valElements: {
				required: "val-required",
				email: "input.val-email",
				integer: "input.val-integer",
				toggle: "input.val-toggle",
				login: "input.val-login",
				password: "input.val-password",
				passtogle: ".password-toggle",
				passdisplay: ".password-display"
				
			},
			regexp: {
				email: /^[-0-9a-z!#$%&'*+\/=?^_`{|}~]+(?:\.[-a-z0-9!#$%&'*+\/=?^_`{|}~]+)*@(?:[a-z0-9]([-a-z0-9]{0,61}[a-z0-9])?\.)+(?:museum|travel|(?:[a-z]{2,4}))$/i,
				integer: /^-?\d+$/,
				login: /^\s*[\w-]{4,32}\s*$/,
				password: /^[\x20-\x7e]{4,32}$/
			},
			
			prototype: {
				
				init: function () {
					(function (validator) {
						
						$(validator.form).submit(function(){return validator.submitForm();});						
						
						validator.email.blur(function(){ validator.validateText(this, $.val.regexp.email);});
						validator.email.keyup(function(){ validator.validateText(this, $.val.regexp.email);});
						
						validator.login.blur(function(){ validator.validateText(this, $.val.regexp.login);});
						validator.login.keyup(function(){ validator.validateText(this, $.val.regexp.login);});
						
						validator.password.blur(function(){ validator.validateText(this, $.val.regexp.password);});
						validator.password.keyup(function(){ validator.validateText(this, $.val.regexp.password);});
						
												
						validator.integer.blur(function(){ validator.validateInteger(this, $.val.regexp.integer,0,2999);});						
						validator.integer.keyup(function(){ validator.validateInteger(this, $.val.regexp.integer,0,2999);});
						
						validator.toggle.click(function(){ validator.validateToggle(this); });
						
					})(this);
				},
				validateText: function(element, regexp) {
					if (element.value == ""){
						if ($(element).hasClass($.val.valElements.required)) {this.showError(element); return false;}	
						else  {this.showDefault(element); return true;}
					}
					if (regexp.test(element.value)) {this.showValid(element); return true;}
					
					this.showError(element); return false;							
				},				
				validateInteger:function(element, regexp, min, max){
					if (element.value == ""){
						if ($(element).hasClass($.val.valElements.required)) {this.showError(element); return false;}	
						else  {this.showDefault(element); return true;}
					}
					if (regexp.test(element.value)) {	
						if ((element.value >= min) && (element.value <= max)) {
							this.showValid(element); return true;
						}
						else {this.showError(element); return false;}
					}
					this.showError(element); return false;				
				},				
				validateToggle:function(element) {
					if ($(element).hasClass($.val.valElements.required)) {
						if (!$(element).attr('checked')) { this.showError(element); return false;}
						else {this.showValid(element); return true; }
					}
					return true;
				},
				submitForm:function(){
					var send = true;
					(function (validator) {
						
						validator.email.each(function(){
							if (!validator.validateText(this,$.val.regexp.email)){send = false;}
						});
						
						validator.integer.each(function(){
							if (!validator.validateInteger(this,$.val.regexp.integer,0,2999)){send = false;}
						});
						
						validator.toggle.each(function(){
							if (!validator.validateToggle(this)){send = false;}
						});
						
						validator.login.each(function(){
							if (!validator.validateText(this,$.val.regexp.login)){send = false;}
						});
						
						validator.password.each(function(){
							if (!validator.validateText(this,$.val.regexp.password)){send = false;}
						});
						
						/*отладочная функция*/
						if (!send) {$(validator.form).css('border','3px solid red');}
						/*отладочная функция*/					
					})(this);
					
					return send;
				},
				showError: function(element) { this.showError(element); },				
				showValid: function(element) { this.showValid(element); },				
				showDefault: function(element) { this.showValid(element); }				
			}
		}
);
})(jQuery);