import { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { Send, TerminalSquare, User, Cpu } from 'lucide-react';

function App() {
  const [mensaje, setMensaje] = useState('');
  const [historial, setHistorial] = useState([
    { 
      rol: 'agente', 
      texto: 'CONSOLA DE IA MULTI-AGENTE INICIADA. \n\nPuedes ingresar operaciones matemáticas, o solicitar las estadísticas de uso.', 
      tipo: 'info' 
    }
  ]);
  const [cargando, setCargando] = useState(false);
  
  // Referencia para el auto-scroll
  const finalChatRef = useRef(null);

  // Efecto para scrollear hacia abajo cada vez que cambia el historial
  useEffect(() => {
    finalChatRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [historial]);

  const enviarMensaje = async (e) => {
    e.preventDefault();
    if (!mensaje.trim()) return;

    const nuevoMensajeUsuario = { rol: 'usuario', texto: mensaje };
    setHistorial((prev) => [...prev, nuevoMensajeUsuario]);
    setMensaje('');
    setCargando(true);

    try {
      // 🚀 MAGIA PURA: Solo enviamos el mensaje. El orquestador decide qué hacer.
      const respuesta = await axios.post('http://127.0.0.1:8000/api/chat', {
        mensaje: nuevoMensajeUsuario.texto
      });

      const mensajeAgente = {
        rol: 'agente',
        texto: respuesta.data.respuesta,
        tipo: respuesta.data.status === 'error' ? 'error' : 'normal'
      };

      setHistorial((prev) => [...prev, mensajeAgente]);
    } catch (error) {
      setHistorial((prev) => [...prev, { rol: 'agente', texto: 'ERROR 500: Backend inalcanzable. Revisa si Uvicorn está corriendo.', tipo: 'error' }]);
    } finally {
      setCargando(false);
    }
  };

  return (
    <div className="min-h-screen bg-black text-cyan-500 font-mono flex items-center justify-center selection:bg-cyan-500 selection:text-black p-4">
      
      {/* Contenedor Principal Centrado */}
      <main className="w-full max-w-4xl bg-black border border-cyan-500/30 rounded-sm shadow-[0_0_30px_rgba(6,182,212,0.1)] flex flex-col h-[85vh]">
        
        {/* Header Cyberpunk */}
        <header className="p-6 border-b border-cyan-500/30 text-center flex flex-col items-center bg-zinc-950/50">
          <h1 className="text-3xl font-bold flex items-center justify-center gap-3 text-cyan-400 drop-shadow-[0_0_15px_#22d3ee] uppercase tracking-wider">
            <TerminalSquare size={36} className="drop-shadow-[0_0_10px_#06b6d4]" />
            Calculadora Futurista Multi-Agente
          </h1>
          <p className="text-zinc-500 mt-2 tracking-[0.3em] text-xs">Llama 3.1 // FastAPI // PostgreSQL // React</p>
        </header>

        {/* Área de Mensajes */}
        <div className="flex-grow p-6 overflow-y-auto space-y-6">
          {historial.map((msg, index) => (
            <div key={index} className={`flex ${msg.rol === 'usuario' ? 'justify-end' : 'justify-start'}`}>
              
              <div className={`flex items-start gap-3 max-w-[85%] ${msg.rol === 'usuario' ? 'flex-row-reverse' : 'flex-row'}`}>
                
                {/* Ícono Neón */}
                <div className={`p-2 rounded-sm border shrink-0 mt-1 ${
                  msg.rol === 'usuario' 
                    ? 'bg-zinc-900 border-zinc-700 text-zinc-400' 
                    : msg.tipo === 'info'
                      ? 'bg-black border-cyan-700 text-cyan-700'
                      : 'bg-cyan-500/10 border-cyan-400 text-cyan-400 shadow-[0_0_15px_#22d3ee]'
                }`}>
                  {msg.rol === 'usuario' ? <User size={20} /> : <Cpu size={20} className="drop-shadow-[0_0_8px_#06b6d4]" />}
                </div>

                { /* Burbuja de Texto */}
                <div className={`p-4 rounded-sm border whitespace-pre-wrap break-words ${
                  msg.rol === 'usuario' 
                    ? 'bg-zinc-950 border-cyan-900 text-cyan-600' 
                    : msg.tipo === 'error'
                      ? 'bg-red-950 border-red-500 text-red-400 [text-shadow:0_0_8px_#ef4444] shadow-[0_0_15px_#ef4444]'
                      : msg.tipo === 'info'
                        ? 'bg-black border-cyan-400 text-cyan-300 font-bold [text-shadow:0_0_10px_#22d3ee,0_0_20px_#22d3ee] shadow-[0_0_15px_rgba(34,211,238,0.4),inset_0_0_15px_rgba(34,211,238,0.2)]'
                        : 'bg-black border-cyan-500/40 text-cyan-400 [text-shadow:0_0_5px_#06b6d4] shadow-[inset_0_0_15px_#06b6d4]'
                }`}>
                  <p className="leading-relaxed font-semibold tracking-wide">{msg.texto}</p>
                </div>
              </div>
            </div>
          ))}

          {/* Spinner de Carga */}
          {cargando && (
            <div className="flex justify-start">
              <div className="bg-black border border-cyan-500/40 p-4 rounded-sm flex gap-3 items-center text-cyan-400 shadow-[inset_0_0_20px_#06b6d4]">
                <Cpu className="animate-spin" size={18} />
                <span className="text-sm tracking-widest animate-pulse [text-shadow:0_0_8px_#22d3ee]">calcular...</span>
              </div>
            </div>
          )}
          {/* Div invisible para el auto-scroll */}
          <div ref={finalChatRef} />
        </div>

        {/* Input Form */}
        <form onSubmit={enviarMensaje} className="p-5 bg-black border-t border-cyan-500/30 flex gap-4">
          <input
            type="text"
            className="flex-grow px-4 py-3 bg-[#0a0a0a] rounded-sm border border-cyan-700 text-cyan-400 focus:outline-none focus:border-cyan-400 focus:shadow-[0_0_20px_#06b6d4,inset_0_0_10px_#06b6d4] transition-all placeholder-cyan-900 font-semibold"
            placeholder="> Ingresa tu petición (ej. Divide 50 entre 2, ¿cuántos errores hay?)..."
            value={mensaje}
            onChange={(e) => setMensaje(e.target.value)}
            disabled={cargando}
            autoFocus
          />
          <button
            type="submit"
            disabled={cargando || !mensaje.trim()}
            className="bg-cyan-500 text-black px-8 py-3 rounded-sm font-bold tracking-wider hover:bg-cyan-400 hover:shadow-[0_0_25px_#22d3ee] transition-all disabled:bg-cyan-950 disabled:text-cyan-800 flex items-center justify-center gap-2"
          >
            ENVIAR <Send size={20} />
          </button>
        </form>
      </main>
    </div>
  );
}

export default App;