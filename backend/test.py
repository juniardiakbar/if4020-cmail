import algorithms.feistel as feistel
import algorithms.sm2_dsa as sign
import algorithms.sm2 as sm2
import algorithms.ecc as ecc

if __name__ == '__main__':
    message = str.encode("ini message tes ke 12 Asif, Irfan, Ijun, Faiz, Hanif, Abda, dan Jofy yang baru")
    uid = str.encode("robinnginx@gmail.com")
    sm2_dsa = sign.SM2_DSA()
 
    sk = 86782133779597314100417424949666102433009022147076393528313227919997331086286
    pk_x = 62039246435999868104268940004814161143349042160397762911796512278334576678030
    pk_y = 10887287044232327482828471478751093935929289214040058352536705741195986414686

    pk = ecc.ECC(a=sm2_dsa._a, b=sm2_dsa._b, field=sm2_dsa._RF_q, x=pk_x, y=pk_y)

    # print(type(sk))
    # print("KUNCI", type(pk), "a=",pk.a, "b=",pk.b, "f=",pk.field, "x=",pk.x, "y=",pk.y)
    # print("DUP KUNCI", type(duplicate_key), "a=",duplicate_key.a, "b=",duplicate_key.b, "f=",duplicate_key.field, "x=",duplicate_key.x, "y=",duplicate_key.y)
    print(sk)
    sign = sm2_dsa.sign(message, uid, sk)
    
    sign_str = str(int.from_bytes(sign[0], "little")) + ';' + str(int.from_bytes(sign[1], "little"))

    sign_str = "89070021666963078306731744112986670786041184797192173663213028137238619628100;44706430561981190424188072797260890933121673409684092434118967442189030565092"

    print(sign_str)

    t1, t2 = sign_str.split(';')
    t1 = int(t1).to_bytes(max(8, (int(t1).bit_length() + 7) // 8), "little")
    t2 = int(t2).to_bytes(max(8, (int(t2).bit_length() + 7) // 8), "little")

    test_tuple = (bytes(t1), bytes(t2))

    print(sm2_dsa.verify(message, test_tuple, uid, pk))