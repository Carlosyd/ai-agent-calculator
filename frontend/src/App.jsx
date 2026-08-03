import { useState } from 'react';
import axios from 'axios';
import { Send, TerminalSquare, User, Cpu, Calculator, MinusCircle, PackagePlus, Divide, TrendingUp } from 'lucide-react';

function App() {
  const [mensaje, setMensaje] = useState('');
  const [herramientaSeleccionada, setHerramientaSeleccionada] = useState(null);
  const [historial, setHistorial] = useState([
    { rol: 'agente', texto: 'CONSOLA DE AGENTES INICIADA. Local Llama 3.1 online. Seleccione una operación del menú.', tipo: 'charla_normal' }
  ]);
  const [cargando, setCargando] = useState(false);

  // Catálogo de herramientas que coinciden con tu backend
  const herramientas = [
    { id: 'suma', nombre: 'SUMA', icono: Calculator, prompt: '>_ Herramienta SUMA seleccionada. Esperando números...' },
    { id: 'resta', nombre: 'RESTA', icono: MinusCircle, prompt: '>_ Herramienta RESTA seleccionada. Ingresa los parámetros...' },
    { id: 'multiplicacion', nombre: 'MULTIPLICACIÓN', icono: PackagePlus, prompt: '>_ Herramienta MULTIPLICACIÓN activa. Ingresa valores...' },
    { id: 'division', nombre: 'DIVISIÓN', icono: Divide, prompt: '>_ Herramienta DIVISIÓN seleccionada. Ingresa el dividendo...' },
    { id: 'probabilidad_momio', nombre: 'PROBABILIDAD', icono: TrendingUp, prompt: '>_ ANALÍTICA DEPORTIVA. Ingresa el momio americano (ej. -150 o +130)...' },
  ];

  const seleccionarHerramienta = (id) => {
    const herramienta = herramientas.find(h => h.id === id);
    setHerramientaSeleccionada(herramienta);
    // Le informamos al usuario de forma automática
    setHistorial([...historial, { rol: 'agente', texto: herramienta.prompt, tipo: 'info' }]);
  };

  const enviarMensaje = async (e) => {
    e.preventDefault();
    if (!mensaje.trim()) return;

    const nuevoMensajeUsuario = { rol: 'usuario', texto: mensaje };
    setHistorial((prev) => [...prev, nuevoMensajeUsuario]);
    setMensaje('');
    setCargando(true);

    // Mandamos el mensaje *y* la pista de la herramienta
    try {
      const respuesta = await axios.post('http://127.0.0.1:8000/api/chat', {
        mensaje: nuevoMensajeUsuario.texto,
        herramienta_sugerida: herramientaSeleccionada ? herramientaSeleccionada.id : null
      });

      const mensajeAgente = {
        rol: 'agente',
        texto: respuesta.data.respuesta,
        tipo: respuesta.data.tipo
      };

      setHistorial((prev) => [...prev, mensajeAgente]);
    } catch (error) {
      setHistorial((prev) => [...prev, { rol: 'agente', texto: 'ERROR 404: Backend inalcanzable. Reiniciando servidor local.', tipo: 'error' }]);
    } finally {
      setCargando(false);
    }
  };

  return (
    <div className="min-h-screen bg-black text-green-500 font-mono flex items-stretch selection:bg-green-500 selection:text-black">
      
      {/* Sidebar de Menú (Herramientas) */}
      <aside className="w-1/4 bg-black border-r border-green-500/30 p-8 flex flex-col gap-6">
        <h2 className="text-xl font-bold text-green-400 drop-shadow-[0_0_10px_rgba(74,222,128,0.8)] uppercase tracking-wider mb-4">
          <Calculator size={28} className="inline mr-2" />
          MENÚ_OPERACIONES
        </h2>
        
        {herramientas.map((h) => {
          const Icon = h.icono;
          const isSelected = herramientaSeleccionada && herramientaSeleccionada.id === h.id;
          return (
            <button
              key={h.id}
              onClick={() => seleccionarHerramienta(h.id)}
              className={`p-4 rounded-sm border transition-all flex items-center gap-3 font-bold text-sm tracking-wider uppercase ${
                isSelected 
                  ? 'bg-green-500 text-black shadow-[0_0_20px_#4ade80]' 
                  : 'bg-black border-green-700 text-green-700 hover:bg-green-950 hover:border-green-500 hover:text-green-500'
              }`}
            >
              <Icon size={18} />
              {h.nombre}
            </button>
          );
        })}
      </aside>

      {/* Área Principal (Chat) */}
      <main className="flex-grow bg-black flex flex-col h-[700px]">
        {/* Header Cyberpunk */}
        <header className="p-8 text-center flex flex-col items-center">
          <h1 className="text-3xl font-bold flex items-center justify-center gap-3 text-green-400 drop-shadow-[0_0_15px_#4ade80] uppercase tracking-wider">
            <TerminalSquare size={36} className="drop-shadow-[0_0_10px_#22c55e]" />
            AGENTE_MATEMÁTICO_V1.0
          </h1>
          <p className="text-zinc-500 mt-2 tracking-[0.3em] text-xs">Llama 3.1 // FastAPI // React</p>
        </header>

        {/* Área de Mensajes */}
        <div className="flex-grow px-8 p-6 overflow-y-auto space-y-6">
          {historial.map((msg, index) => (
            <div key={index} className={`flex ${msg.rol === 'usuario' ? 'justify-end' : 'justify-start'}`}>
              
              <div className={`flex items-start gap-3 max-w-[85%] ${msg.rol === 'usuario' ? 'flex-row-reverse' : 'flex-row'}`}>
                
                {/* Ícono Neón */}
                <div className={`p-2 rounded-sm border ${
                  msg.rol === 'usuario' 
                    ? 'bg-zinc-900 border-zinc-700 text-zinc-400' 
                    : msg.tipo === 'info'
                      ? 'bg-black border-green-700 text-green-700'
                      : 'bg-green-500/10 border-green-400 text-green-400 shadow-[0_0_15px_#4ade80]'
                }`}>
                  {msg.rol === 'usuario' ? <User size={20} /> : <Cpu size={20} className="drop-shadow-[0_0_8px_#22c55e]" />}
                </div>

                { /* Burbuja de Texto */}
                <div className={`p-4 rounded-sm border ${
                  msg.rol === 'usuario' 
                    ? 'bg-zinc-950 border-green-900 text-green-600' 
                    : msg.tipo === 'error'
                      ? 'bg-red-950 border-red-500 text-red-400 [text-shadow:0_0_8px_#ef4444] shadow-[0_0_15px_#ef4444]'
                      : msg.tipo === 'info'
                        ? 'bg-black border-green-400 text-green-300 font-bold [text-shadow:0_0_10px_#4ade80,0_0_20px_#4ade80] shadow-[0_0_15px_rgba(74,222,128,0.4),inset_0_0_15px_rgba(74,222,128,0.2)]'
                        : 'bg-black border-green-500/40 text-green-400 [text-shadow:0_0_5px_#22c55e] shadow-[inset_0_0_15px_#22c55e]'
                }`}>
                  <p className="leading-relaxed font-semibold tracking-wide">{msg.texto}</p>
                </div>
              </div>

            </div>
          ))}

          {/* Spinner de Carga */}
          {cargando && (
            <div className="flex justify-start">
              <div className="bg-black border border-green-500/40 p-4 rounded-sm flex gap-3 items-center text-green-400 shadow-[inset_0_0_20px_#22c55e]">
                <Cpu className="animate-spin" size={18} />
                <span className="text-sm tracking-widest animate-pulse [text-shadow:0_0_8px_#4ade80]">PROCESANDO_DATOS...</span>
              </div>
            </div>
          )}
        </div>

        {/* Input Form */}
        <form onSubmit={enviarMensaje} className="p-5 bg-black border-t border-green-500/30 flex gap-4">
          <input
            type="text"
            className="flex-grow px-4 py-3 bg-[#0a0a0a] rounded-sm border border-green-700 text-green-400 focus:outline-none focus:border-green-400 focus:shadow-[0_0_20px_#22c55e,inset_0_0_10px_#22c55e] transition-all placeholder-green-900 font-semibold"
            placeholder={herramientaSeleccionada ? herramientaSeleccionada.prompt : '> Escribe parámetros...'}
            value={mensaje}
            onChange={(e) => setMensaje(e.target.value)}
            disabled={cargando}
          />
          <button
            type="submit"
            disabled={cargando || !mensaje.trim()}
            className="bg-green-500 text-black px-6 py-3 rounded-sm font-bold tracking-wider hover:bg-green-400 hover:shadow-[0_0_25px_#4ade80] transition-all disabled:bg-green-950 disabled:text-green-800 flex items-center justify-center"
          >
            <Send size={20} />
          </button>
        </form>
      </main>
    </div>
  );
}

export default App;