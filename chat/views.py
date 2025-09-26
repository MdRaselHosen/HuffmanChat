from django.shortcuts import render, redirect
from chat.huffman import huffman_encode, huffman_decode

def chat_view(request):
    # Get chat history from session, or initialize if not present
    chat_history = request.session.get("chat_history", [])

    # ✅ Handle reset
    if request.method == "POST" and "reset" in request.POST:
        chat_history = []
        request.session["chat_history"] = chat_history
        return redirect("chat")  # redirect to clear form and refresh page

    # ✅ Handle message sending
    if request.method == "POST" and "message" in request.POST:
        message = request.POST.get("message", "").strip()
        if message:
            encoded, codes, original_size, compressed_size = huffman_encode(message)
            decoded_message = huffman_decode(encoded, codes)

            chat_history.append({
                "original": message,
                "decoded": decoded_message,
                "original_size": original_size,
                "compressed_size": compressed_size
            })
            request.session["chat_history"] = chat_history  # Save back to session

    return render(request, "index.html", {"chat_history": chat_history})