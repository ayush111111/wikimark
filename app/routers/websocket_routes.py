from typing import Set
from fastapi import WebSocket,WebSocketDisconnect, WebSocketException, APIRouter, Depends
from ..users import current_active_user
from ..services.async_wikipedia_client import async_wiki_client

ws_router = APIRouter(prefix="/websocket",tags=["Websocket"])
# connection manager
class Manager:
    def __init__(self):
        self.active_connections : Set[WebSocket] = set()
    async def connect(self, websocket:WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)
        print(f"Websocket connected. Total connections: {len(self.active_connections)}")     

    def disconnect(self, websocket:WebSocket):
        self.active_connections.discard(websocket)
        print(f"Websocket disconnected. Total connections: {len(self.active_connections)}")        

manager = Manager()
# endpoint
@ws_router.websocket("/ws/search")
async def websocket_search(
    websocket : WebSocket,
):
    await manager.connect(websocket=websocket)

    try:
        while True:
            data = websocket.receive_json()
            query = data.get("query", "")

            if not query:
                websocket.send_json({"type": "error", "message": "Query cannot be empty"})

            await websocket.send_json({"type": "search_start", "query": query})

            results  = await async_wiki_client.search_with_fallback(query=query)

            for i,res in enumerate(results):
                await websocket.send_json(
                    {
                        "type": "result",
                        "data" : res,
                        "index": i,
                        "total": len(results)
                    }
                )
            
            await websocket.send_json({"type":"search_end", "total": len(results)})

    except WebSocketDisconnect as e:
        manager.disconnect(websocket=websocket)
    except Exception as e:
        try:
           websocket.send_json({"type":"error", "total": len(results)})
        except:
            pass
    

# router = 


