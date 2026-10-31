import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Lock, Mail, ArrowRight } from 'lucide-react';
import toast from 'react-hot-toast';
import api from '../api';

function Login({ onLoginSuccess, onSwitchToSignup }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      console.log('Iniciando login para:', email);
      const formData = new FormData();
      formData.append('username', email);
      formData.append('password', password);

      const response = await api.post('/token', formData);
      console.log('Login realizado com sucesso:', response.data);
      const { access_token } = response.data;

      localStorage.setItem('token', access_token);
      toast.success('Bem-vindo de volta!');
      onLoginSuccess();
    } catch (err) {
      console.error('Erro detalhado no login:', err);
      const errorMsg = err.response?.data?.detail || 'Erro ao fazer login. Verifique suas credenciais.';
      toast.error(typeof errorMsg === 'string' ? errorMsg : 'Erro inesperado ao fazer login.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center p-6 font-sans">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-md w-full bg-white p-10 rounded-3xl shadow-xl border border-slate-100"
      >
        <div className="text-center mb-10">
          <div className="w-16 h-16 bg-indigo-600 rounded-2xl flex items-center justify-center text-white shadow-lg shadow-indigo-200 mx-auto mb-4">
            <Lock className="w-8 h-8" />
          </div>
          <h2 className="text-3xl font-black text-slate-800 tracking-tight">Bem-vindo ao <span className="text-indigo-600">FinFlow</span></h2>
          <p className="text-slate-500 mt-2">Acesse sua conta para gerenciar suas finanças</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="space-y-2">
            <label className="text-sm font-bold text-slate-700 ml-1">E-mail</label>
            <div className="relative">
              <Mail className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full pl-12 pr-4 py-3 bg-slate-50 border border-slate-200 rounded-2xl focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition-all text-slate-800"
                placeholder="seu@email.com"
              />
            </div>
          </div>

          <div className="space-y-2">
            <label className="text-sm font-bold text-slate-700 ml-1">Senha</label>
            <div className="relative">
              <Lock className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full pl-12 pr-4 py-3 bg-slate-50 border border-slate-200 rounded-2xl focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition-all text-slate-800"
                placeholder="••••••••"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-4 bg-indigo-600 text-white rounded-2xl font-bold hover:bg-indigo-700 transition-all shadow-lg shadow-indigo-200 flex items-center justify-center gap-2 group"
          >
            {loading ? 'Entrando...' : 'Entrar'}
            {!loading && <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />}
          </button>
        </form>

        <div className="mt-8 text-center">
          <p className="text-slate-500 text-sm">
            Não tem uma conta?{' '}
            <button
              onClick={onSwitchToSignup}
              className="text-indigo-600 font-bold hover:underline transition-all"
            >
              Crie uma agora
            </button>
          </p>
        </div>
      </motion.div>
    </div>
  );
}

export default Login;
