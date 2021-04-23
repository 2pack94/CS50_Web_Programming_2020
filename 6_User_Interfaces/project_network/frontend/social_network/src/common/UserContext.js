import React from 'react';

// This Context contains information about the current user that should be available in many Components.
// The Context values here are just defaults and get populated in the App Component.
export const UserContext = React.createContext({
    id: 0,
    is_authenticated: false,
    username: "",
    getUser: () => {},
    resetUser: () => {}
});

export const DELETED_USER_NAME = 'deleted_user';
