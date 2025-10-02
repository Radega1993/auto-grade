import React from 'react';
import { useAuthStore } from '../stores/authStore';

const DebugAuth: React.FC = () => {
  const { user, tokens, isAuthenticated, getToken } = useAuthStore();

  return (
    <div className="fixed top-4 right-4 bg-black text-white p-4 rounded-lg text-xs max-w-sm">
      <h3 className="font-bold mb-2">Debug Auth State:</h3>
      <div className="space-y-1">
        <div>Authenticated: {isAuthenticated ? 'YES' : 'NO'}</div>
        <div>User: {user ? `${user.first_name} ${user.last_name}` : 'None'}</div>
        <div>Token: {getToken() ? 'Present' : 'Missing'}</div>
        <div>Token Preview: {getToken()?.substring(0, 20)}...</div>
      </div>
    </div>
  );
};

export default DebugAuth;
