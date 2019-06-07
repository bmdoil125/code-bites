const randomstring = require('randomstring');

const username = randomstring.generate();
const email = `${username}@test.com`;


describe('Login', () => {
    it('display login form', () => {
        cy
            .visit('/login')
            .get('h1').contains('Login')
            .get('form');
    })

    it('user allowed to sign in', () => {
        //register user first
        cy
            .visit('/register')
            .get('input[name="username"]').type(username)
            .get('input[name="email"]').type(email)
            .get('input[name="password"]').type('test')
            .get('input[type="submit"]').click()

        // signout
        cy.get('.navbar-burger').click()
        cy.contains('Signout').click()

        // log back in
        cy
            .get('a').contains('Login').click()
            .get('input[name="email"]').type(email)
            .get('input[name="password"]').type('test')
            .get('input[type="submit"]').click()
            .wait(100)
        // Expect redirect to "/"
        cy.contains('All Users')
        cy.contains(username)
        cy.get('.navbar-burger').click()
        cy.get('.navbar-menu').within(() => {
            cy
                .get('.navbar-item').contains('Profile')
                .get('.navbar-item').contains('Signout')
                .get('.navbar-item').contains('Login').should('not.be.visible')
                .get('.navbar-item').contains('Register').should('not.be.visible')
        });

        // signout again
        cy.get('.navbar-burger').click()
        cy.get('a').contains('Signout').click()

        // /signout displayed properly
        cy.get('p').contains('Signed Out')
        cy.get('navbar-menu').within(() => {
            cy
                .get('.navbar-item').contains('Signout').should('not.be.visible')
                .get('.navbar-item').contains('Login')
                .get('.navbar-item').contains('Register')
        })
    });
});